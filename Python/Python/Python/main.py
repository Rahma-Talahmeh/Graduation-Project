from vehicle_detector import detect_vehicle
from parking_status import has_space
from gate_controller import open_gate, close_gate
import time

print(" Smart Parking System Started")

while True:
    vehicle_detected = detect_vehicle()  
    if vehicle_detected:
        print("car arrives")

        if has_space():
            open_gate()
            print("✅barrier open")
        else:
            print("❌There are no places")
            close_gate()
            print("🔒barrier closed")

    time.sleep(1) 
