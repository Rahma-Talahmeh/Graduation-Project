# Smart Parking System

## Project Overview
The Smart Parking System is a prototype designed to manage parking availability using computer vision, sensors, and microcontroller-based control. The system detects incoming vehicles using a camera, checks parking availability, and automatically controls a gate barrier. Additionally, it provides real-time parking status using LEDs and an LCD screen.

This project demonstrates the feasibility of integrating software and hardware components into a functional smart parking solution.

---

## System Architecture
The system is divided into two main components:

### 1. Hardware (ESP32)
- ESP32 microcontroller
- Servo motor for gate control
- IR / LDR sensors for parking spot detection
- LEDs (Red / Green) to indicate parking status
- 16x2 LCD to display parking availability

### 2. Software (Python)
- web-based application, allowing users to access its services anytime and from anywhere through an internet connection
- OpenCV used for vehicle detection via camera
- EasyOCR used for automatic license plate recognition by extracting text from detected license plate images
- YOLOv8 used for detecting and tracking vehicles in parking areas through real-time image analysis.
- Serial communication with ESP32 to send gate control commands

 
## Key Features
- Vehicle detection using a camera (OpenCV)
- Automatic gate control using a servo motor
- Parking availability calculation using sensors
- Real-time status display on LCD screen
- Visual indication using red and green LEDs
- Serial communication between Python application and ESP32

---
## Screenshots

![Plate Recognition](images/plate%20number%20and%20vehicle%20recognition.jpg)

*Vehicle detection and license plate recognition using YOLOv8 and EasyOCR*

![Barrier open](images/barrier_open.jpeg)

*Barrier open*

![Login Page](images/Login.jpg)

*User login interface*

![Find Owner](images/find%20owner.jpg)

*Search and display vehicle owner information*

![Find Vehicle](images/find%20vehicle.jpg)

*Search for a vehicle using its plate number*

![Sensor response and LED activation](images/sensor_led.jpeg)

*Sensor response and LED activation*

![Screen displays the parking state when there are two spots available](images/parking_state.jpeg)

*Screen displays the parking state when there are two spots available*

![Full Parking State](images/full%20parking%20state.jpg)

*Screen displays the parking state when all spots are occupied*

![Screen displays the parking state when it is full](images/parking_state_full.jpeg)

*Screen displays the parking state when it is full*


![Barrier closed](images/barrier_closed.jpeg)  
*Barrier closed*
---

## Technologies Used
- Python (OpenCV, PySerial, EasyOCR, YOLOv8)
- Arduino IDE
- ESP32 Microcontroller
- GitHub for version control

---

## Notes
This project represents a functional prototype developed during GP1. The implemented components demonstrate the feasibility of the proposed system architecture and serve as a foundation for further development in GP2.
