import time
from collections import deque

import cv2
import numpy as np
import serial

from data_frame import frame_build

ser = serial.Serial(
    port="COM26",
    baudrate=115200,
)
parts = 5
blur = 7
threshold = 23
scale = 0.8
close_kernel = 46
fps_history = deque(maxlen=30)
global filtered_off

# 初始化 PID 参数
P, I, D = 0, 0, 0


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


def nothing(x):
    pass


cv2.namedWindow("Trackbars")
cv2.createTrackbar("parts", "Trackbars", parts, 10, nothing)
cv2.createTrackbar("scale", "Trackbars", int(scale * 100), 100, nothing)
cv2.createTrackbar("blur", "Trackbars", blur, 50, nothing)
cv2.createTrackbar("threshold", "Trackbars", threshold, 100, nothing)
cv2.createTrackbar("close_kernel", "Trackbars", close_kernel, 100, nothing)


def frame_cut(frame, num_parts, scale):
    """
    图像切割函数
    """
    height, width = frame.shape[:2]
    part_height = height // num_parts
    cutted_frames = []

    for i in range(num_parts):
        start_row = i * part_height
        if i == num_parts - 1:
            end_row = height
        else:
            end_row = (i + 1) * part_height
        cutted_frame = frame[
            start_row:end_row,
            int(width * (1 - scale) / 2) : int(width * (1 + scale) / 2),
        ]
        cutted_frames.append(cutted_frame)

    return cutted_frames


def get_center(frames, blur_kernel, threshold, close_kernel):
    """
    处理，获取中心
    """
    centers = []

    for frame in frames:
        if blur_kernel % 2 == 0:
            blur_kernel += 1

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (blur_kernel, blur_kernel), 0)
        edges = cv2.Canny(blurred, threshold, 150)

        kernel = np.ones((close_kernel, close_kernel), np.uint8)
        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        cv2.imshow("edges", edges)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if contours:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                centers.append((cX, cY))
            else:
                centers.append((None, None))
        else:
            centers.append((None, None))
    return centers


def line(frame, centers, scale, parts):
    """
    连接中心,计算偏移量
    """
    prev_center = None
    # 基准线
    cv2.line(
        frame,
        (frame.shape[1] // 2, 0),
        (frame.shape[1] // 2, frame.shape[0]),
        (0, 0, 255),
        2,
    )
    off_history = []
    filtered_off = 0
    height, width = frame.shape[:2]  # 在函数内部定义 height 和 width
    for i, (cX, cY) in enumerate(centers):
        if cX is not None and cY is not None:
            part_height = height // parts
            part_width = int(width * (1 - scale) / 2)
            start_row = i * part_height
            center = (cX + part_width, start_row + cY)
            cv2.circle(frame, (cX + part_width, start_row + cY), 5, (255, 0, 0), -1)
            if prev_center is not None:
                cv2.line(frame, prev_center, center, (0, 255, 0), 2)
            prev_center = center

            # 偏移量
            off = width // 2 - cX - part_width
            off_history.append(off)
    if len(off_history) != 0:
        filtered_off = sum(off_history) // len(off_history)
    cv2.line(
        frame,
        (width // 2 - filtered_off, 0),
        (width // 2 - filtered_off, height),
        (255, 0, 0),
        1,
    )
    # print(filtered_off)
    return filtered_off


speed_history = []


def main():
    global P, I, D
    cap = cv2.VideoCapture(0)
    while True:
        start_time = time.time()
        ret, frame = cap.read()
        if not ret:
            break

        # 滑条读取
        parts = cv2.getTrackbarPos("parts", "Trackbars")  # 垂直分割的数量
        scale = cv2.getTrackbarPos("scale", "Trackbars") / 100  # 水平限幅
        blur_kernel = cv2.getTrackbarPos("blur", "Trackbars")  # 高斯模糊核
        threshold = cv2.getTrackbarPos("threshold", "Trackbars")  # 边缘检测阈值
        close_kernel = cv2.getTrackbarPos("close_kernel", "Trackbars")  # 闭运算核

        cutted_frames = frame_cut(frame, parts, scale)
        centers = get_center(cutted_frames, blur_kernel, threshold, close_kernel)

        filtered_off = line(frame, centers, scale, parts)

        # 读取键盘输入的 PID 参数
        key = cv2.waitKey(1) & 0xFF
        if key == ord("p"):
            P = int(input("输入 P 值: "))
        elif key == ord("i"):
            I = int(input("输入 I 值: "))
        elif key == ord("d"):
            D = int(input("输入 D 值: "))

        # 打包并发送数据
        data = frame_build(filtered_off, P, I, D)
        ser.write(data)

        end_time = time.time()

        fps = 1 / (end_time - start_time)
        fps_history.append(fps)
        avg_fps = sum(fps_history) / len(fps_history)
        # print(f"FPS: {int(avg_fps)}")
        cv2.putText(
            frame,
            f"FPS: {int(avg_fps)}",
            (5, 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2,
        )

        cv2.imshow("frame", frame)

        if key == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
