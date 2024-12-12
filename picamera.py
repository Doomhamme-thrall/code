from time import sleep

from picamera import PiCamera

camera = PiCamera()

# 启动摄像头预览
camera.start_preview()

# 等待2秒以确保摄像头稳定
sleep(2)

# 捕获图像
camera.capture("/home/pi/image.jpg")

# 停止摄像头预览
camera.stop_preview()
