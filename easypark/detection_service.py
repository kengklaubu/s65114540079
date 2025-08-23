import cv2
import torch
from django.apps import apps
from easypark.utils import update_parking_status  # ฟังก์ชันสำหรับอัปเดตสถานะ
import threading

is_active = False  # ตัวแปรควบคุมสถานะการทำงานของการตรวจจับ
detection_thread = None  # เก็บ Thread ของการตรวจจับ
current_location = None  # เก็บ location ปัจจุบัน
stop_event = threading.Event()  # ใช้หยุดเธรด
CONFIDENCE_THRESHOLD = 0.40

_model = None  # เก็บโมเดลในตัวแปร Global

def load_model():
    global _model
    if _model is None:  # โหลดครั้งเดียว
        try:
            _model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
            # กำหนดค่า confidence threshold หลังจากโหลดโมเดล
            _model.conf = CONFIDENCE_THRESHOLD
        except Exception as e:
            print(f"❌ Error loading YOLOv5 model: {e}")
            _model = None
    return _model


def get_camera_url(location_id):
    ParkingLocation = apps.get_model('easypark', 'ParkingLocation')
    try:
        location = ParkingLocation.objects.get(id=location_id)
        return location.camera_url
    except ParkingLocation.DoesNotExist:
        return None
    except Exception as e:
        print(f"⚠️ Error retrieving camera URL: {e}")
        return None

def get_rois_from_db(location_id):
    ROI = apps.get_model('easypark', 'ROI')
    ParkingLocation = apps.get_model('easypark', 'ParkingLocation')

    try:
        location = ParkingLocation.objects.get(id=location_id)
        rois = ROI.objects.filter(location=location, parking_spot__location=location)

        roi_list = []
        for roi in rois:
            spot = roi.parking_spot
            if spot:
                roi_list.append((spot.spot_number, roi.x_position, roi.y_position, roi.width, roi.height))

        return roi_list
    except ParkingLocation.DoesNotExist:
        return []
    except Exception as e:
        print(f"❌ Error retrieving ROIs: {e}")
        return []
    

def start_detection_in_background(selected_location):
    global is_active, detection_thread, current_location, stop_event

    # ถ้ากำลังตรวจจับที่เดิม -> ไม่ต้องเริ่มใหม่
    if is_active and current_location == selected_location:
        print("⚠️ Detection is already running at the same location. Ignoring request.")
        return  

    # ถ้ากำลังตรวจจับที่อื่นอยู่ -> หยุดเธรดเก่า
    if is_active and current_location != selected_location:
        print(f"🔄 Changing location from {current_location} to {selected_location}. Restarting detection...")
        stop_detection()

    # เริ่มการตรวจจับใหม่
    is_active = True  
    current_location = selected_location
    stop_event.clear()  # รีเซ็ต stop_event ให้ทำงานใหม่ได้
    detection_thread = threading.Thread(target=detect_cars, args=(int(selected_location),), daemon=True)
    detection_thread.start()
    print(f"🚗 Starting detection for location: {selected_location}")

def stop_detection():
    global is_active, detection_thread, stop_event

    if is_active:
        print(f"🛑 Stopping detection at location {current_location}...")
        is_active = False
        stop_event.set()  # แจ้งให้เธรดหยุดทำงาน

        if detection_thread is not None:
            detection_thread.join()  # รอให้เธรดหยุดก่อน
        detection_thread = None
        print("✅ Detection fully stopped.")

def detect_cars(selected_location):
    global is_active
    print(f"🚗 Starting detection for location: {selected_location}")

    model = load_model()
    if not model:
        print("❌ Model loading failed. Aborting detection.")
        return

    camera_url = get_camera_url(selected_location)
    if not camera_url:
        print(f"❌ No camera URL for location {selected_location}. Stopping detection.")
        is_active = False
        return

    cap = cv2.VideoCapture(camera_url)
    if not cap.isOpened():
        print(f"❌ Unable to open camera: {camera_url}")
        is_active = False
        return

    current_rois = get_rois_from_db(selected_location)
    if not current_rois:
        print(f"❌ No ROIs defined for location: {selected_location}")
        return

    while not stop_event.is_set():  # ทำงานต่อเมื่อ stop_event ไม่ถูกตั้งค่า
        ret, frame = cap.read()
        if not ret:
            break

        # เรียกใช้โมเดลโดยไม่ส่ง conf parameter
        results = model(frame)
        detections = results.pandas().xyxy[0]  

        update_parking_status(current_rois, detections, selected_location)

        if stop_event.is_set():  
            break  

        if cv2.waitKey(3000) & 0xFF == ord('q'):  
            break  

    cap.release()
    cv2.destroyAllWindows()
    print(f"🚗 Detection stopped for location: {selected_location}")

