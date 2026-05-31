from vehicle_detector import detect_vehicle
from parking_status import has_space
from gate_controller import open_gate, close_gate
import time

print("🚗 Smart Parking System Started")

while True:
    vehicle_detected = detect_vehicle() 
    if vehicle_detected:
        print("🚗 سيارة وصلت")

        if has_space():
            open_gate()
            print("✅ الحاجز مفتوح")
        else:
            print("❌ لا يوجد أماكن")
            close_gate()
            print("🔒 الحاجز مغلق")

    time.sleep(1) ا
