import cv2
import numpy as np
import serial

upper_hsv = np.array([153, 255, 255])
lower_hsv = np.array([64, 72, 49])

cap = cv2.VideoCapture(0)
# ser = serial.Serial("COM5", 9600, timeout=0.1)

while True:
    ret, frame = cap.read()
    if not ret:
        break

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

            cv2.circle(frame, center, radius, (0, 255, 0), 3)
            cv2.putText(
                frame,
                f"Area: {int(area)}",
                (center[0] + radius, center[1]),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                2,
            )

            # ser.write(f"{center[0]} {center[1]}\n".encode())

    cv2.imshow("mask", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
