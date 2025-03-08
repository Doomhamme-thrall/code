import cv2
import numpy as np


def process_frame(frame):
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    _, binary = cv2.threshold(l, 25, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow("Binary_before", binary)

    kernel = np.ones((22, 22), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    cv2.imshow("Binary_after", binary)

    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
    # contours = [
    #     contour for contour in contours if 500 <= cv2.contourArea(contour) <= 2000
    # ]

    cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
    return frame


def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        processed_frame = process_frame(frame)
        cv2.imshow("Line Follower", processed_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
