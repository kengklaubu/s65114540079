from easypark.models import ParkingSpot

def update_parking_status(rois, detections, location):
    """
    อัปเดตสถานะช่องจอดรถในฐานข้อมูล

    Args:
        rois (list): รายการของ ROI (spot_number, x, y, w, h)
        detections (DataFrame): Bounding boxes จาก YOLOv5
        location (str): ชื่อ Location ของช่องจอด
    """
    for roi in rois:
        spot_number, x, y, w, h = roi

        # ตรวจสอบการทับซ้อนระหว่าง bounding box และ ROI
        detected = False
        for _, row in detections.iterrows():
            label = row['name']
            x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])

            if label == 'car' and (x1 < x + w and x2 > x and y1 < y + h and y2 > y):  # ตรวจสอบการทับซ้อน
                detected = True
                break

        # อัปเดตสถานะในฐานข้อมูล
        try:
            parking_spot = ParkingSpot.objects.get(spot_number=spot_number, location__name=location)  # เชื่อม location
            parking_spot.is_available = not detected  # ว่างถ้าไม่มีรถ
            parking_spot.save()  # บันทึกการเปลี่ยนแปลง
        except ParkingSpot.DoesNotExist:
            print(f"Parking spot {spot_number} in location {location} does not exist.")
