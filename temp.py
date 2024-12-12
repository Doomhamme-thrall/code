import cv2
import numpy as np


def detect_color(frame, lower_bound, upper_bound):
    # 转换为HSV颜色空间
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # 去除噪点
    ##############


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

        # 如何找到色块位置
        ############################

        # 显示结果
        cv2.imshow("Frame", frame)
        cv2.imshow("Mask Blue", mask_blue)
        cv2.imshow("Mask Red", mask_red)
        cv2.imshow("Mask Green", mask_green)

    # 释放摄像头并关闭所有窗口
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
