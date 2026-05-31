import cv2
from ultralytics import YOLO
import easyocr
import threading
from datetime import datetime
import serial
import time
import re
import mysql.connector
import requests

# ================= DATABASE =================
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Yasmeen2004.",
        database="parking_system"
    )

# ================= Arduino =================
try:
    ser = serial.Serial('COM4', 9600, timeout=1)
    time.sleep(2)
    print("✅ Connected to ESP32")
except:
    print("❌ ESP32 not connected")
    ser = None

# ================= AI =================
model = YOLO('yolov8n.pt')
model.fuse()

reader = easyocr.Reader(['en'])

# ================= Camera =================
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

current_plate = "Scanning..."
system_message = ""

last_open_time = 0
last_detect_time = 0

COOLDOWN = 5

recorded_plates = set()

# ================= Gate =================
def send_open_command():

    global last_open_time

    current_time = time.time()

    if ser and (current_time - last_open_time > COOLDOWN):

        ser.write(b'OPEN\n')

        print("📨 OPEN command sent")

        last_open_time = current_time


def send_register_message():

    if ser:
        ser.write(b'REGISTER\n')
        print("📨 REGISTER message sent")


def send_full_message():

    if ser:
        ser.write(b'FULL\n')
        print("📨 FULL message sent")

# ================= DATABASE CHECK =================
def is_registered(plate):

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT *
        FROM Vehicles
        WHERE plate_number=%s
    """, (plate,))

    result = cursor.fetchone()

    db.close()

    return result is not None

# ================= PARKING CHECK =================
def has_available_spots():

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM Parking_Spots
        WHERE status='available'
    """)

    count = cursor.fetchone()[0]

    db.close()

    return count > 0

# ================= OCR =================
def ocr_worker(car_crop):

    global current_plate
    global system_message
    global last_detect_time

    # يمنع القراءة المتكررة بسرعة
    if time.time() - last_detect_time < 2:
        return

    last_detect_time = time.time()

    # تصغير الصورة لتسريع OCR
    small = cv2.resize(car_crop, (320, 240))

    results = reader.readtext(small)

    for (bbox, text, prob) in results:

        if prob > 0.55:

            # تنظيف النص
            plate_text = re.sub(r'[^A-Z0-9]', '', text.upper())

            # تجاهل النصوص القصيرة
            if len(plate_text) < 3:
                continue

            current_plate = plate_text
            last_detected_plate = plate_text

            print("🚗 Plate:", plate_text)

            # ===============================
            # السيارة مسجلة
            # ===============================
            if is_registered(plate_text):

                if has_available_spots():

                    system_message = "Access Granted"

                    # فتح الحاجز
                    send_open_command()

                    # ===============================
                    # ربط اللوحة مع السبوت
                    # ===============================
                    try:

                        requests.post(
                            "http://172.18.231.11:8000/bind-spot",
                            json={
                                "plate": plate_text,
                                "spot": 2
                            },
                            timeout=2
                        )

                        print("✅ Plate linked to spot")

                    except Exception as e:
                        print("❌ Bind failed:", e)

                else:

                    system_message = "Parking Full"

                    send_full_message()

            # ===============================
            # السيارة غير مسجلة
            # ===============================
            else:

                system_message = "Registration Required - Scan QR"

                send_register_message()

            # ===============================
            # حفظ اللوحات
            # ===============================
            if plate_text not in recorded_plates:

                with open("plates_log.txt", "a") as f:

                    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    f.write(f"{dt} | {plate_text}\n")

                recorded_plates.add(plate_text)

            # يمنع التكرار
            break

# ================= MAIN =================
print("🚗 Smart Parking AI Started")

while True:

    ret, frame = cap.read()

    if not ret:
        continue

    # car, motorcycle, bus, truck
    results = model(frame, classes=[2,3,5,7], verbose=False)

    for result in results:

        for box in result.boxes:

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # رسم مربع السيارة
            cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)

            # عرض رقم اللوحة
            cv2.putText(
                frame,
                f"Plate: {current_plate}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0,255,0),
                2
            )

            # عرض رسالة النظام
            cv2.putText(
                frame,
                system_message,
                (30, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,255),
                3
            )

            # OCR Thread
            if threading.active_count() < 2:

                car_img = frame[y1:y2, x1:x2]

                threading.Thread(
                    target=ocr_worker,
                    args=(car_img,),
                    daemon=True
                ).start()

    cv2.imshow("Smart Parking AI", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ================= END =================
cap.release()

if ser:
    ser.close()

cv2.destroyAllWindows()
