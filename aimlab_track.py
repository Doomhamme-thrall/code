from os import error
import cv2
import numpy as np
import time
import ctypes

lower_rgb = np.array([101, 28, 0])
upper_rgb = np.array([217, 121, 116])
blur = 1
open_kernel = 2

def nothing(x):
    pass


cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FPS, 120)

# PID控制器类
class PID:
    def __init__(self, Kp=0.5, Ki=0.0, Kd=0.1):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.last_error = 0
        self.integral = 0
        self.last_time = None

    def compute(self, error):
        now = time.time()
        dt = now - self.last_time if self.last_time else 0.008  # 默认120fps
        self.last_time = now
        if abs(self.integral) < 1000:
            self.integral += error * dt
        derivative = (error - self.last_error) / dt if dt > 0 else 0
        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        self.last_error = error
        return output


class MouseMover:
    def __init__(self):
        self.SendInput = ctypes.windll.user32.SendInput

    def move(self, dx, dy):
        class MOUSEINPUT(ctypes.Structure):
            _fields_ = [
                ("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
            ]
        class INPUT(ctypes.Structure):
            _fields_ = [
                ("type", ctypes.c_ulong),
                ("mi", MOUSEINPUT),
            ]
        mi = MOUSEINPUT(dx, dy, 0, 0x0001, 0, None)  # 0x0001 = MOUSEEVENTF_MOVE
        inp = INPUT(0, mi)
        self.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))


mouse = MouseMover()
pid_x = PID(Kp=0.9, Ki=0.01, Kd=0.012)
pid_y = PID(Kp=0.9, Ki=0.01, Kd=0.012)




prev_frame = None
while True:
    time_start = time.time()
    ret, frame = cap.read()
    if not ret or (prev_frame is not None and np.array_equal(frame, prev_frame)):
        break

    (high, width) = frame.shape[:2]
    frame_cx = width // 2
    frame_cy = high // 2

    error_x = 0
    error_y = 0

    gaus_mask = cv2.inRange(frame, lower_rgb, upper_rgb)
    contours, _ = cv2.findContours(gaus_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 50 and area < 15000:
                hull = cv2.convexHull(contour)
                center, radius = cv2.minEnclosingCircle(hull)
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

                # 计算窗口中心与center的误差
                error_x = center[0] - frame_cx
                error_y = center[1] - frame_cy

                move_x = pid_x.compute(error_x)
                move_y = pid_y.compute(error_y)

                if abs(error_x) > 20 or abs(error_y) > 20:
                    mouse.move(int(move_x), int(move_y))
                prev_frame = frame.copy()
                break
    else:
        mouse.move(error_x, 0)
        prev_frame = frame.copy()

    time_end = time.time()
    print(f"fps:{1 / (time_end - time_start):.2f}")
    cv2.imshow("aimhsv", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()