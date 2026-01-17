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
- Python application running on a PC
- OpenCV used for vehicle detection via camera
- Serial communication with ESP32 to send gate control commands

---

## Project Structure
