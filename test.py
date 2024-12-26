import cv2


def record_video(output_filename, codec="XVID", fps=20.0, resolution=(640, 480)):
    # 打开默认摄像头
    cap = cv2.VideoCapture(0)

    # 检查摄像头是否成功打开
    if not cap.isOpened():
        print("无法打开摄像头")
        return

    # 定义视频编解码器并创建 VideoWriter 对象
    fourcc = cv2.VideoWriter_fourcc(*codec)
    out = cv2.VideoWriter(output_filename, fourcc, fps, resolution)

    print("按 'q' 键停止录制")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("无法接收帧 (stream end?). Exiting ...")
            break

        # 写入帧到视频文件
        out.write(frame)

        # 显示帧
        cv2.imshow("Recording", frame)

        # 按 'q' 键退出录制
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # 释放资源
    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    output_filename = "output.avi"
    record_video(output_filename)
