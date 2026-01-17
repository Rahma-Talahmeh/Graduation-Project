import serial
import time

COM_PORT = 'COM3'
BAUD_RATE = 9600

def open_gate():
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    ser.write(b'OPEN\n')
    ser.close()

def close_gate():
    # لو عندك أمر للإغلاق على ESP32
    pass
