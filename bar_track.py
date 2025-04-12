import math
import time

import cv2
import numpy as np
import serial

from data_frame import frame_build


class pid_data:
    def __init__(self):
        pid_data.p = 0
        pid_data.i = 0
        pid_data.d = 0


lower_lab = np.array([0, 158, 88])
upper_lab = np.array([171, 239, 232])
positions = []
blur = 41
open_kernel = 46


def nothing(x):
    pass


cv2.namedWindow("Trackbars")
cv2.createTrackbar("H_low", "Trackbars", lower_lab[0], 180, nothing)
cv2.createTrackbar("S_low", "Trackbars", lower_lab[1], 255, nothing)
cv2.createTrackbar("V_low", "Trackbars", lower_lab[2], 255, nothing)
cv2.createTrackbar("H_high", "Trackbars", upper_lab[0], 180, nothing)
cv2.createTrackbar("S_high", "Trackbars", upper_lab[1], 255, nothing)
cv2.createTrackbar("V_high", "Trackbars", upper_lab[2], 255, nothing)
cv2.createTrackbar("open_kernel", "Trackbars", open_kernel, 255, nothing)
cv2.createTrackbar("blur", "Trackbars", blur, 255, nothing)


cap = cv2.VideoCapture(0)
ser = serial.Serial("COM5", 115200, timeout=0.1)

speed_history = []


def low_pass_filter(data, window_size=5, order=3):
    """
    多阶低通滤波器，过滤异常点
    :param data: 输入数据列表
    :param window_size: 滑动窗口大小
    :param order: 滤波器阶数（应用次数）
    :return: 当前滤波后的数据
    """
    if not data:
        return None

    # Step 1: Calculate the median and median absolute deviation (MAD)
    median = np.median(data)
    mad = np.median([abs(x - median) for x in data])

    # Step 2: Define a threshold for outlier detection
    threshold = 3 * mad  # Adjust the multiplier as needed

    # Step 3: Filter out outliers
    filtered_data = [x for x in data if abs(x - median) <= threshold]

    # Step 4: Apply the low-pass filter
    for _ in range(order):
        filtered_data = [
            sum(filtered_data[max(0, i - window_size + 1) : i + 1])
            / len(filtered_data[max(0, i - window_size + 1) : i + 1])
            for i in range(len(filtered_data))
        ]

    # Return the last value as the current filtered data
    return filtered_data[-1] if filtered_data else None


# def read_keyboard_input():
#     while True:
#         try:
#             values = input("pid:").split()
#             if len(values) == 3:
#                 pid.p, pid.i, pid.d = map(float, values)
#         except ValueError:
#             pass


# input_thread = threading.Thread(target=read_keyboard_input)
# input_thread.daemon = True
# input_thread.start()


def get_speed(x, y):
    x -= 500
    y -= 228  # 坐标系变换

    x *= 43 / 500
    y *= 21.5 / 230  # 映射为实际坐标

    lenth = math.sqrt(x**2 + y**2)
    if x < 0:
        lenth = -lenth
    print(f"lenth: {lenth}")

    current_time = time.time()

    positions.append((lenth, current_time))
    if len(positions) > 3:
        positions.pop(0)

    if positions[-1][1] - positions[0][1] != 0:
        lenth_speed = (positions[-1][0] - positions[0][0]) / (
            positions[-1][1] - positions[0][1]
        )
        speed_history.append(lenth_speed)
        if len(speed_history) > 60:
            speed_history.pop(0)
        speed = low_pass_filter(speed_history)
        print(f"speed: {speed}")
        frame = frame_build(int(lenth), int(speed))
        ser.write(frame)


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

    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

    blurred = cv2.GaussianBlur(lab, (blur, blur), 0)
    gaus_mask = cv2.inRange(blurred, lower_lab, upper_lab)

    # kernel = np.ones((open_kernel, open_kernel), np.uint8)
    # open_mask = cv2.morphologyEx(gaus_mask, cv2.MORPH_CLOSE, kernel)

    # 背景减法器
    # bg_subtractor = cv2.createBackgroundSubtractorMOG2(
    #     history=500, varThreshold=50, detectShadows=True
    # )
    # fg_mask = bg_subtractor.apply(open_mask)

    return gaus_mask


def find_contours(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 600 and area < 15000:
            hull = cv2.convexHull(contour)

            center, radius = cv2.minEnclosingCircle(hull)  # 最小外接圆
            center = (int(center[0]), int(center[1]))
            radius = int(radius)

            cv2.circle(frame, center, radius, (0, 255, 0), 2)

            cv2.putText(
                frame,
                f"({center[0]}, {center[1]}, {area})",
                (center[0] - 20, center[1] - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )
            get_speed(center[0], center[1])


while True:
    ret, frame = cap.read()
    if not ret:
        break

    lower_lab[0] = cv2.getTrackbarPos("H_low", "Trackbars")
    lower_lab[1] = cv2.getTrackbarPos("S_low", "Trackbars")
    lower_lab[2] = cv2.getTrackbarPos("V_low", "Trackbars")
    upper_lab[0] = cv2.getTrackbarPos("H_high", "Trackbars")
    upper_lab[1] = cv2.getTrackbarPos("S_high", "Trackbars")
    upper_lab[2] = cv2.getTrackbarPos("V_high", "Trackbars")
    blur = cv2.getTrackbarPos("blur", "Trackbars")
    # open_kernel = cv2.getTrackbarPos("open_kernel", "Trackbars")

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
