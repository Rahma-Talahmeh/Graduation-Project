# ESP32 Parking Controller

## Description
This module runs on an **ESP32** and controls the parking lot status display and gate servo. It reads sensors for parking spots, updates LEDs and LCD, and opens the gate when a command is received from the main system (e.g., camera or web app).  

---

## Features
- **Parking Sensors** – Detects if a parking spot is available using digital sensors.  
- **LED Indicators** – Green LED for available, Red LED for occupied.  
- **LCD Display** – Shows number of available spots or "Parking Full".  
- **Gate Control (Servo)** – Opens the gate when receiving the `OPEN` command via Serial.  
- **Serial Communication** – Receives commands from main system (e.g., `OPEN`).  

---

## Hardware Setup
- **ESP32 pins**:  
  - LCD: 14, 27, 26, 25, 33, 32  
  - Servo: 18  
  - Sensors: 23, 22, 21, 19  
  - Green LEDs: 5, 17, 16, 4  
  - Red LEDs: 2, 15, 13, 12  

---

## How to Run
1. Upload the code to ESP32 using Arduino IDE.  
2. Connect all sensors, LEDs, LCD, and servo according to pin assignments.  
3. Power the ESP32. The LCD will show parking status.  
4. Send `"OPEN"` via Serial to open the gate if spots are available.  

---

## Notes / To-Do
- Future integration with **camera license plate detection** for automatic gate control.  
- Adjust gate opening time or sensor sensitivity as needed.  
