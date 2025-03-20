import cv2


def list_available_cameras(max_cameras=20):
    available_cameras = []
    for i in range(max_cameras):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available_cameras.append(i)
            cap.release()
        else:
            print("cammera", i, "cant use")
    return available_cameras


if __name__ == "__main__":
    cameras = list_available_cameras()
    if cameras:
        print("Available cameras:", cameras)
    else:
        print("No cameras found.")
