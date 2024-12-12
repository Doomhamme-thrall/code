import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
from pyzbar import pyzbar
from time import sleep


def decode_qr_code(frame):
    # 使用pyzbar库解码二维码
    decoded_objects = pyzbar.decode(frame)
    for obj in decoded_objects:
        # 获取二维码信息
        qr_data = obj.data.decode("utf-8")
        print(f"QR Code detected: {qr_data}")
        return qr_data
    return None


def detect_colors(frame):
    # 转换为HSV颜色空间
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 定义颜色范围
    color_ranges = {
        "Blue": ((100, 150, 0), (140, 255, 255)),
        "Red": ((0, 150, 0), (10, 255, 255)),
        "Green": ((40, 150, 0), (80, 255, 255)),
    }

    for color_name, (lower, upper) in color_ranges.items():
        mask = cv2.inRange(hsv, lower, upper)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:  # 只考虑大于500像素的区域
                x, y, w, h = cv2.boundingRect(contour)
                print(
                    f"Detected {color_name} color block at (x: {x}, y: {y}, width: {w}, height: {h}) with area {area}"
                )


def main():
    # 初始化摄像头
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    raw_capture = PiRGBArray(camera, size=(640, 480))

    # 让摄像头预热
    sleep(2)

    for frame in camera.capture_continuous(
        raw_capture, format="bgr", use_video_port=True
    ):
        image = frame.array

        # 识别二维码
        qr_data = decode_qr_code(image)
        if qr_data:
            print(f"QR Code Data: {qr_data}")

        # 进行颜色识别
        detect_colors(image)

        # 显示帧
        cv2.imshow("Frame", image)

        # 按下'q'键退出
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        # 清除流以准备下一个帧
        raw_capture.truncate(0)

    # 释放摄像头并关闭窗口
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
