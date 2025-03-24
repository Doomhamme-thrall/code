import cv2
import numpy as np
import torch
from pyzbar import pyzbar

model = torch.hub.load("ultralytics/yolov5", "custom", path="best.pt")

animal_labels = [
    "turtle",
    "octopus",
    "shark",
]


def decode_qr_code(frame, qr_detected):
    if qr_detected:
        return None
    decoded_objects = pyzbar.decode(frame)
    for obj in decoded_objects:
        qr_data = obj.data.decode("utf-8")
        print(f"QR Code detected: {qr_data}")
        return qr_data
    return None


def detect_colors(frame, last_color):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    color_ranges = {
        "Blue": ((100, 150, 0), (140, 255, 255)),
        "Red": ((0, 150, 0), (10, 255, 255)),
        "Green": ((40, 150, 0), (80, 255, 255)),
    }

    detected_colors = []
    for color_name, (lower, upper) in color_ranges.items():
        mask = cv2.inRange(hsv, lower, upper)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:
                x, y, w, h = cv2.boundingRect(contour)
                detected_colors.append(color_name)
                if color_name != last_color:
                    print(
                        f"Detected {color_name} color block at (x: {x}, y: {y}, width: {w}, height: {h}) with area {area}"
                    )
    return detected_colors


def detect_animals(frame, last_animal):
    results = model(frame)
    labels, cords = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
    n = len(labels)
    detected_animals = []
    for i in range(n):
        row = cords[i]
        if row[4] >= 0.5:  # 置信度阈值
            x1, y1, x2, y2 = (
                int(row[0] * frame.shape[1]),
                int(row[1] * frame.shape[0]),
                int(row[2] * frame.shape[1]),
                int(row[3] * frame.shape[0]),
            )
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            animal_name = animal_labels[int(labels[i])]
            detected_animals.append(animal_name)
            if animal_name != last_animal:
                cv2.putText(
                    frame,
                    f"{animal_name}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 255, 0),
                    2,
                )
                print(f"Detected animal: {animal_name}")
    return detected_animals


def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("camera error")
        return

    qr_detected = False
    last_color = None
    last_animal = None

    while True:
        ret, frame = cap.read()

        if not ret:
            print("frame error")
            break

        qr_data = decode_qr_code(frame, qr_detected)
        if qr_data:
            print(f"QR Code Data: {qr_data}")
            qr_detected = True

        detected_colors = detect_colors(frame, last_color)
        if detected_colors:
            last_color = detected_colors[0]

        detected_animals = detect_animals(frame, last_animal)
        if detected_animals:
            last_animal = detected_animals[0]
        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
