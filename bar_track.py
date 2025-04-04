import math
import queue
import threading
import time

import cv2
import numpy as np

from data_frame import frame_build


class pid_data:
    def __init__(self):
        pid_data.p = 0
        pid_data.i = 0
        pid_data.d = 0


lower_hsv = np.array([20, 34, 119])
upper_hsv = np.array([146, 183, 212])
positions = []
blur = 7
open_kernel = 46


def nothing(x):
    pass


cv2.namedWindow("Trackbars")


# cv2.createTrackbar("H_low", "Trackbars", lower_hsv[0], 180, nothing)
# cv2.createTrackbar("S_low", "Trackbars", lower_hsv[1], 255, nothing)
# cv2.createTrackbar("V_low", "Trackbars", lower_hsv[2], 255, nothing)
# cv2.createTrackbar("H_high", "Trackbars", upper_hsv[0], 180, nothing)
# cv2.createTrackbar("S_high", "Trackbars", upper_hsv[1], 255, nothing)
# cv2.createTrackbar("V_high", "Trackbars", upper_hsv[2], 255, nothing)
cv2.createTrackbar("open_kernel", "Trackbars", open_kernel, 100, nothing)
cv2.createTrackbar("blur", "Trackbars", blur, 100, nothing)

pid = pid_data()


cap = cv2.VideoCapture(1)
# ser = serial.Serial("COM5", 9600, timeout=0.1)


input_queue = queue.Queue()


def read_keyboard_input():
    while True:
        try:
            values = input("pid:").split()
            if len(values) == 3:
                pid.p, pid.i, pid.d = map(float, values)
        except ValueError:
            pass


input_thread = threading.Thread(target=read_keyboard_input)
input_thread.daemon = True
input_thread.start()


def get_speed(x, y):
    x -= 320
    y -= 240  # 中心原点

    x *= 1
    y *= 1  # 映射为实际坐标

    lenth = math.sqrt(x**2 + y**2)

    current_time = time.time()

    positions.append((x, y, current_time))
    if len(positions) > 3:
        positions.pop(0)

    if positions[-1][2] - positions[0][2] != 0:
        x_speed = (positions[-1][0] - positions[0][0]) / (
            positions[-1][2] - positions[0][2]
        )
        y_speed = (positions[-1][1] - positions[0][1]) / (
            positions[-1][2] - positions[0][2]
        )
        print(f"x_speed: {x_speed}, y_speed: {y_speed}")
        speed = math.sqrt(x_speed**2 + y_speed**2)
        print(f"speed: {speed}")
        frame = frame_build(int(lenth), int(speed))


def frame_process(frame, blur, open_kernel):
    if blur % 2 == 0:
        blur += 1

    # origin_point = np.float32([[0, 0], [0, 1], [1, 0], [1, 1]])
    # real_point = np.float32([[0, 0], [0, 2], [2, 0], [2, 2]])
    # matrix = cv2.getPerspectiveTransform(origin_point, real_point)
    # transformed_frame = cv2.warpPerspective(
    #     frame, matrix, (frame.shape[1], frame.shape[0])
    # )

    # rota_matrix = cv2.getRotationMatrix2D(center, 0, 1)  # 旋转
    # frame = cv2.warpAffine(rota_matrix, rota_matrix, (width, high))

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    blurred = cv2.GaussianBlur(hsv, (blur, blur), 0)
    gaus_mask = cv2.inRange(blurred, lower_hsv, upper_hsv)

    kernel = np.ones((open_kernel, open_kernel), np.uint8)
    open_mask = cv2.morphologyEx(gaus_mask, cv2.MORPH_CLOSE, kernel)

    # 背景减法器
    # bg_subtractor = cv2.createBackgroundSubtractorMOG2(
    #     history=500, varThreshold=50, detectShadows=True
    # )
    # fg_mask = bg_subtractor.apply(open_mask)

    return open_mask


def find_contours(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 3000 and area < 15000:
            center, radius = cv2.minEnclosingCircle(contour)
            circularity = 4 * np.pi * area / (cv2.arcLength(contour, True) ** 2)
            if circularity > 0.8:
                x, y = int(center[0]), int(center[1])
                cv2.circle(frame, (x, y), int(radius), (0, 255, 0), 2)
                cv2.putText(
                    frame,
                    f"({x}, {y},{area})",
                    (x - 20, y - 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2,
                )
                get_speed(x, y)


while True:
    ret, frame = cap.read()
    if not ret:
        break

    # lower_hsv[0] = cv2.getTrackbarPos("H_low", "Trackbars")
    # lower_hsv[1] = cv2.getTrackbarPos("S_low", "Trackbars")
    # lower_hsv[2] = cv2.getTrackbarPos("V_low", "Trackbars")
    # upper_hsv[0] = cv2.getTrackbarPos("H_high", "Trackbars")
    # upper_hsv[1] = cv2.getTrackbarPos("S_high", "Trackbars")
    # upper_hsv[2] = cv2.getTrackbarPos("V_high", "Trackbars")
    blur = cv2.getTrackbarPos("blur", "Trackbars")
    open_kernel = cv2.getTrackbarPos("open_kernel", "Trackbars")

    (high, width) = frame.shape[:2]
    center = (width // 2, high // 2)

    open_mask = frame_process(frame, blur, open_kernel)

    cv2.imshow("mask", open_mask)
    find_contours(open_mask)
    # print(f"{pid.p}{pid.i}{pid.d}")
    # ser.write(f"{pid.p} {pid.i} {pid.d} \n".encode())

    cv2.line(frame, (width // 2, 0), (width // 2, high), (0, 0, 255), 1)
    cv2.line(frame, (0, high // 2), (width, high // 2), (0, 0, 255), 1)
    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        print()
        break
