import cv2
import numpy as np
import serial


class pid_data:
    def __init__(self):
        pid_data.p = 1
        pid_data.i = 0
        pid_data.d = 0
        pid_data.cmd = 0


pid_data = pid_data()

ser = serial.Serial("COM5", 9600, timeout=0.1)

while 1:
    pid_data.p, pid_data.i, pid_data.d, pid_data.cmd = input("pid:").split()
    print(f"{pid_data.p} {pid_data.i} {pid_data.d} {pid_data.cmd}")
    ser.write(
        f"{pid_data.p} {pid_data.i} {pid_data.d} {pid_data.cmd}\n".encode("utf-8")
    )
