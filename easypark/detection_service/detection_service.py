# import cv2
# import torch
# from easypark.models import ParkingSpot, ParkingLocation
# from .utils import update_parking_status  # ถ้ามี utils.py สำหรับฟังก์ชันนี้

# # โหลดโมเดล YOLOv5
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# # ตัวอย่าง ROIs (ขึ้นอยู่กับ Location)
# rois = {
#     "ตึกวิจัย": [
#         (1, 400, 400, 200, 200),
#         (2, 700, 200, 200, 200),
#     ],
#     "โรงพยาบาล": [
#         (1, 300, 300, 200, 200),
#         (2, 600, 200, 200, 200),
#     ],
# }

# def get_camera_url(location_name):
#     """
#     ดึง URL ของกล้องสำหรับ Location ที่เลือก
#     """
#     try:
#         location = ParkingLocation.objects.get(name=location_name)
#         return location.camera_url
#     except ParkingLocation.DoesNotExist:
#         print(f"Location {location_name} does not exist.")
#         return None

# def detect_cars(selected_location):
#     """
#     ตรวจจับรถยนต์ใน Location ที่เลือก และอัปเดตสถานะในฐานข้อมูล
#     """
#     # ดึง URL ของกล้อง
#     camera_url = get_camera_url(selected_location)
#     if not camera_url:
#         print(f"Cannot find camera URL for location: {selected_location}")
#         return

#     cap = cv2.VideoCapture(camera_url)
#     if not cap.isOpened():
#         print(f"Cannot connect to camera for location: {selected_location}")
#         return

#     # เลือก ROIs สำหรับ Location
#     current_rois = rois.get(selected_location, [])
#     if not current_rois:
#         print(f"No ROIs defined for location: {selected_location}")
#         return

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print(f"Cannot read frames from camera for location: {selected_location}")
#             break

#         # ตรวจจับวัตถุ
#         results = model(frame)
#         detections = results.pandas().xyxy[0]  # ดึงข้อมูล bounding boxes

#         # อัปเดตสถานะในฐานข้อมูล
#         update_parking_status(current_rois, detections, selected_location)

#         # Delay ระหว่างการตรวจจับแต่ละครั้ง
#         if cv2.waitKey(1000) & 0xFF == ord('q'):  # ทุก 1 วินาที
#             break

#     cap.release()
#     cv2.destroyAllWindows()
