import queue
import threading

import cv2
import numpy as np
import serial


class pid_data:
    def __init__(self):
        pid_data.p = 0
        pid_data.i = 0
        pid_data.d = 0


lower_hsv = np.array([23, 3, 78])
upper_hsv = np.array([158, 149, 161])


def nothing(x):
    pass


# 创建窗口
cv2.namedWindow("Trackbars")

# 创建滑动条，用于调整红色的HSV上下限
cv2.createTrackbar("H_low", "Trackbars", lower_hsv[0], 180, nothing)
cv2.createTrackbar("S_low", "Trackbars", lower_hsv[1], 255, nothing)
cv2.createTrackbar("V_low", "Trackbars", lower_hsv[2], 255, nothing)
cv2.createTrackbar("H_high", "Trackbars", upper_hsv[0], 180, nothing)
cv2.createTrackbar("S_high", "Trackbars", upper_hsv[1], 255, nothing)
cv2.createTrackbar("V_high", "Trackbars", upper_hsv[2], 255, nothing)

pid = pid_data()


cap = cv2.VideoCapture(0)
# ser = serial.Serial("COM5", 9600, timeout=0.1)


# 图像四角坐标
# src_points = np.array(
#     [[100, 100], [200, 100], [200, 200], [100, 200]], dtype=np.float32
# )
# 真实四角坐标
# dst_points = np.array([[0, 0], [10, 0], [10, 10], [0, 10]], dtype=np.float32)

# perspective_matrix = cv2.getPerspectiveTransform(src_points, dst_points)

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


while True:
    ret, frame = cap.read()
    if not ret:
        break

    lower_hsv[0] = cv2.getTrackbarPos("H_low", "Trackbars")
    lower_hsv[1] = cv2.getTrackbarPos("S_low", "Trackbars")
    lower_hsv[2] = cv2.getTrackbarPos("V_low", "Trackbars")
    upper_hsv[0] = cv2.getTrackbarPos("H_high", "Trackbars")
    upper_hsv[1] = cv2.getTrackbarPos("S_high", "Trackbars")
    upper_hsv[2] = cv2.getTrackbarPos("V_high", "Trackbars")

    (h, w) = frame.shape[:2]
    center = (w // 2, h // 2)

    m = cv2.getRotationMatrix2D(center, 0, 1)  # 旋转矩阵
    frame = cv2.warpAffine(frame, m, (w, h))

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    blurred = cv2.GaussianBlur(hsv, (11, 11), 0)
    mask = cv2.inRange(blurred, lower_hsv, upper_hsv)
    cv2.imshow("mask", mask)

    # lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    # blurred = cv2.GaussianBlur(lab, (11, 11), 0)
    # mask = cv2.inRange(blurred, lower__lab, upper_lab)
    # cv2.imshow("lab", lab)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100:
            retval, triangle = cv2.minEnclosingTriangle(contour)
            triangle = np.int32(triangle)

            cv2.polylines(
                frame, [triangle], isClosed=True, color=(0, 255, 0), thickness=2
            )

            # actual = cv2.perspectiveTransform(
            #     np.array([center], dtype=np.float32).reshape(-1, 1, 2),
            #     perspective_matrix,
            # )
            # x, y = actual[0][0]

            # cv2.circle(frame, center, radius, (0, 255, 0), 3)
            # cv2.putText(
            #     frame,
            #     f"{int(area)},{x, y}",
            #     (center[0] + radius, center[1]),
            #     cv2.FONT_HERSHEY_SIMPLEX,
            #     0.5,
            #     (255, 255, 255),
            #     2,
            # )
            # print(x, y)

            # ser.write(f"{center[0]} {center[1]}\n".encode())

    print(f"{pid.p}{pid.i}{pid.d}")
    # ser.write(f"{pid.p} {pid.i} {pid.d} \n".encode())

    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        print()
        break
