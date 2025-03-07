import cv2
import numpy as np
import serial


class pid_data:
    def __init__(self):
        pid_data.p = 0
        pid_data.i = 0
        pid_data.d = 0


upper_hsv = np.array([153, 255, 255])
lower_hsv = np.array([64, 72, 49])

cap = cv2.VideoCapture(0)
ser = serial.Serial("COM5", 9600, timeout=0.1)


# 图像四角坐标
src_points = np.array(
    [[100, 100], [200, 100], [200, 200], [100, 200]], dtype=np.float32
)
# 真实四角坐标
dst_points = np.array([[0, 0], [10, 0], [10, 10], [0, 10]], dtype=np.float32)

perspective_matrix = cv2.getPerspectiveTransform(src_points, dst_points)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    (h, w) = frame.shape[:2]
    center = (w // 2, h // 2)

    m = cv2.getRotationMatrix2D(center, 0, 1)  # 旋转矩阵
    frame = cv2.warpAffine(frame, m, (w, h))

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    blurred = cv2.GaussianBlur(hsv, (11, 11), 0)
    mask = cv2.inRange(blurred, lower_hsv, upper_hsv)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:
            (x, y), radius = cv2.minEnclosingCircle(contour)
            center = (int(x), int(y))
            radius = int(radius)

            actual = cv2.perspectiveTransform(
                np.array([center], dtype=np.float32).reshape(-1, 1, 2),
                perspective_matrix,
            )
            x, y = actual[0][0]

            cv2.circle(frame, center, radius, (0, 255, 0), 3)
            cv2.putText(
                frame,
                f"{int(area)},{x, y}",
                (center[0] + radius, center[1]),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                2,
            )
            print(x, y)

            # ser.write(f"{center[0]} {center[1]}\n".encode())

    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
