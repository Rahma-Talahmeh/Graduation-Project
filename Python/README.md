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
- Ensure the camera is positioned properly for vehicle detection.  
- `COOLDOWN` can be adjusted to avoid frequent gate opening.  
- Future integration with license plate recognition for automatic vehicle identification.  
