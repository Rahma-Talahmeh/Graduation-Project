import cv2
import time
import serial

# ===== Serial =====
ser = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)  # ESP32 ready

def send_open_command():
    ser.write(b'OPEN\n')
    print("📨 أمر فتح الحاجز أرسل للـ ESP32")

# ===== Camera =====
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

time.sleep(1)

ret, bg = cap.read()
if not ret:
    print("❌ لم يتم فتح الكاميرا")
    exit()

bg_gray = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
print("📷 Vehicle detector ready")

last_open_time = 0
COOLDOWN = 4  # ثواني

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(bg_gray, gray)
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

    motion_pixels = cv2.countNonZero(thresh)

    cv2.imshow("Camera Live", frame)

    current_time = time.time()

    if motion_pixels > 20000 and (current_time - last_open_time) > COOLDOWN:
        print("🚗 سيارة مكتشفة")
        send_open_command()
        last_open_time = current_time
        bg_gray = gray

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
ser.close()
cv2.destroyAllWindows()
