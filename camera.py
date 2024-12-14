import cv2

# 打开摄像头，参数0表示第一个摄像头
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("无法打开摄像头")
    exit()

while True:
    # 读取摄像头的一帧
    ret, frame = cap.read()

    if not ret:
        print("无法接收帧，结束程序")
        break

    # 显示这一帧
    cv2.imshow("USB Camera", frame)

    # 按下'q'键退出
    if cv2.waitKey(1) == ord("q"):
        break

# 释放摄像头并关闭所有窗口
cap.release()
cv2.destroyAllWindows()
