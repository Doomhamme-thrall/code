import cv2

# ser = serial.Serial("COM5", 9600, timeout=0.1)
parts = 2
binary_threshold = 5
kernel_size = 22
scale = 0.9


def nothing(x):
    pass


cv2.namedWindow("Trackbars")
cv2.createTrackbar("parts", "Trackbars", parts, 10, nothing)
cv2.createTrackbar("scale", "Trackbars", int(scale * 100), 100, nothing)
cv2.createTrackbar("blur", "Trackbars", binary_threshold, 50, nothing)
cv2.createTrackbar("edge", "Trackbars", kernel_size, 100, nothing)


def frame_cut(frame, num_parts, scale):
    height, width = frame.shape[:2]
    part_height = height // num_parts
    cutted_frames = []

    for i in range(num_parts):
        start_row = i * part_height
        if i == num_parts - 1:
            end_row = height
        else:
            end_row = (i + 1) * part_height
        cutted_frame = frame[
            start_row:end_row,
            int(width * (1 - scale) / 2) : int(width * (1 + scale) / 2),
        ]
        cutted_frames.append(cutted_frame)

    return cutted_frames


def get_center(frames, blur_kernel, kernel_size):
    centers = []
    for frame in frames:
        if blur_kernel % 2 == 0:
            blur_kernel += 1

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (blur_kernel, blur_kernel), 0)
        edges = cv2.Canny(blurred, kernel_size, 150)

        cv2.imshow("edges", edges)

        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                centers.append((cX, cY))
            else:
                centers.append((None, None))
        else:
            centers.append((None, None))
    return centers


def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        parts = cv2.getTrackbarPos("parts", "Trackbars")
        scale = cv2.getTrackbarPos("scale", "Trackbars") / 100
        blur_kernel = cv2.getTrackbarPos("blur", "Trackbars")
        kernel_size = cv2.getTrackbarPos("edge", "Trackbars")

        cutted_frames = frame_cut(frame, parts, scale)
        centers = get_center(cutted_frames, blur_kernel, kernel_size)

        prev_center = None
        for i, (cX, cY) in enumerate(centers):
            if cX is not None and cY is not None:
                height, width = frame.shape[:2]
                part_height = height // parts
                part_width = int(width * (1 - scale) / 2)
                start_row = i * part_height
                center = (cX + part_width, start_row + cY)
                cv2.circle(frame, (cX + part_width, start_row + cY), 5, (0, 255, 0), -1)
                if prev_center is not None:
                    cv2.line(frame, prev_center, center, (0, 255, 0), 2)
                prev_center = center

        cv2.imshow("frame", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
