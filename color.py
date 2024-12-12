import cv2
import numpy as np


def detect_color(frame, lower_bound, upper_bound):
    # 转换为HSV颜色空间
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # 创建颜色掩码
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    # 进行形态学操作，去除噪点
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    return mask


def main():
    # 打开摄像头
    cap = cv2.VideoCapture(0)

    # 定义颜色范围
    lower_blue = np.array([100, 150, 0])
    upper_blue = np.array([140, 255, 255])

    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])

    lower_green = np.array([40, 40, 40])
    upper_green = np.array([70, 255, 255])

    while True:
        # 读取帧
        ret, frame = cap.read()
        if not ret:
            break

        # 检测颜色
        mask_blue = detect_color(frame, lower_blue, upper_blue)
        mask_red = detect_color(frame, lower_red, upper_red)
        mask_green = detect_color(frame, lower_green, upper_green)

        # 找到颜色块的轮廓
        for mask, color_name in [
            (mask_blue, "Blue"),
            (mask_red, "Red"),
            (mask_green, "Green"),
        ]:
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 500:  # 只考虑大于500像素的区域
                    x, y, w, h = cv2.boundingRect(contour)
                    print(
                        f"Detected {color_name} color block at (x: {x}, y: {y}, width: {w}, height: {h}) with area {area}"
                    )
