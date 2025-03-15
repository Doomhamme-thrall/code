import cv2

cap = cv2.VideoCapture(1)
cap2 = cv2.VideoCapture(0)

while 1:
    ret, frame = cap.read()
    ret2, frame2 = cap2.read()
    if not ret:
        break
    if not ret2:
        break
    cv2.imshow("frame2", frame2)
    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
