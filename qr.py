import cv2
from pyzbar import pyzbar


def decode_qr(frame):
    decoded_objects = pyzbar.decode(frame)
    for obj in decoded_objects:
        print(f"Type: {obj.type}")
        print(f"Data: {obj.data.decode('utf-8')}\n")
    return decoded_objects


def main():
    # 打开默认摄像头
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video device.")
        return

    while True:
        # 读取摄像头帧
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # 解码并打印二维码数据
        decode_qr(frame)

        # 检查用户是否按下了“q”键
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # 释放摄像头资源
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
