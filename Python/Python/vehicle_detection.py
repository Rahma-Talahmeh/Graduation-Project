import cv2
import serial
import time

# ===== Serial =====
ser = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)

# ===== Camera =====
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

ret, bg = cap.read()
bg_gray = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)

print("📷 Camera Ready")

last_send = 0
COOLDOWN = 5  # ثواني

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(bg_gray, gray)
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

    motion = cv2.countNonZero(thresh)
    cv2.imshow("Camera Live", frame)

    now = time.time()
    if motion > 20000 and (now - last_send) > COOLDOWN:
        print(" Car Detected → OPEN")
        ser.write(b'OPEN\n')
        last_send = now
        bg_gray = gray

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
ser.close()
cv2.destroyAllWindows()
