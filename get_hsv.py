import cv2
import numpy as np

LAB_min = np.array([118, 34, 119])
LAB_max = np.array([146, 149, 161])

x_before = 0
y_before = 0


def get_LAB_value(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        LAB_value = LAB_frame[y, x]
        print(x, 480 - y)
        print(47 * (x / 640))
        global x_before, y_before
        print(x - x_before, y - y_before)
        print(f"LAB: {LAB_value}")
        global LAB_min, LAB_max
        LAB_min = np.minimum(LAB_min, LAB_value)
        LAB_max = np.maximum(LAB_max, LAB_value)
        x_before = x
        y_before = y


cap = cv2.VideoCapture(1)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    # LAB_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    LAB_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

    cv2.imshow("Frame", frame)
    cv2.imshow("LAB", LAB_frame)
    cv2.setMouseCallback("Frame", get_LAB_value)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

print(f"LAB min: {LAB_min}")
print(f"LAB max: {LAB_max}")
cap.release()
cv2.destroyAllWindows()
