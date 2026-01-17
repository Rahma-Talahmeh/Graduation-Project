# Smart Parking Python Controller

## Description
This Python module connects the **camera** to the **ESP32 parking controller**. It detects vehicles in real-time using OpenCV, checks parking availability, and sends commands to the ESP32 to open or close the gate.  

---

## Features
- **Vehicle Detection** – Uses camera feed to detect cars approaching the parking lot.  
- **Parking Status Check** – Reads parking availability using the `has_space()` function.  
- **Gate Control** – Sends `"OPEN"` command via Serial to ESP32 if a spot is available.  
- **Cooldown Mechanism** – Prevents multiple gate openings in a short period.  
- **Live Camera Feed** – Displays live camera stream with motion detection.  

---

## How to Run
1. Install required Python packages:
```bash
pip install opencv-python pyserial
```
2. Connect ESP32 to the computer via USB (update `COM_PORT` if needed).  
3. Run the script:
```bash
python main.py
```
4. The system will detect cars and automatically open the gate if spots are available.  
5. Press `q` to stop the camera feed.  

---

## Notes / To-Do
The current camera module performs **vehicle detection only** based on motion detection.
- License plate recognition is **not implemented yet**.
- Future work includes integrating **OCR (Optical Character Recognition)** to detect the **vehicle plate number** after a car is detected.
- The OCR module will extract and return the plate number to be used for gate control and system logging.
