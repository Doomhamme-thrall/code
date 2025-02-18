from ultralytics import YOLO

model = YOLO("yolov5s.pt")

results = model(r"C:\Users\Administrator\Pictures\Screenshots\1.png")

for result in results:
    print(result)

for result in results:
    result.show()
