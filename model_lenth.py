import cv2
import numpy as np
import os

# 加载标定结果
calibration_file = "stereo_calibration.npz"
if not os.path.exists(calibration_file):
    print(f"标定文件 {calibration_file} 不存在，请先完成标定！")
    exit()

data = np.load(calibration_file)
mtx_left = data['mtx_left']
dist_left = data['dist_left']
mtx_right = data['mtx_right']
dist_right = data['dist_right']
R = data['R']  # 旋转矩阵
T = data['T']  # 平移向量

# 基线距离（单位：米）
baseline = abs(T[0, 0])

# 提供左右拍摄图像路径
left_image_path = "captured_images/left_007.jpg"
right_image_path = "captured_images/right_007.jpg"

if not os.path.exists(left_image_path) or not os.path.exists(right_image_path):
    print(f"图像文件 {left_image_path} 或 {right_image_path} 不存在！")
    exit()

# 加载图像
left_image = cv2.imread(left_image_path)
right_image = cv2.imread(right_image_path)

# 校正图像
map_left_1, map_left_2 = cv2.initUndistortRectifyMap(
    mtx_left, dist_left, None, mtx_left, left_image.shape[:2][::-1], cv2.CV_16SC2)
map_right_1, map_right_2 = cv2.initUndistortRectifyMap(
    mtx_right, dist_right, None, mtx_right, right_image.shape[:2][::-1], cv2.CV_16SC2)

left_undistorted = cv2.remap(left_image, map_left_1, map_left_2, cv2.INTER_LINEAR)
right_undistorted = cv2.remap(right_image, map_right_1, map_right_2, cv2.INTER_LINEAR)

# 加载深度学习立体匹配模型
model_path = "path_to_your_model.onnx"  # 替换为你的模型路径
if not os.path.exists(model_path):
    print(f"模型文件 {model_path} 不存在，请下载或训练模型！")
    exit()

# 加载模型
net = cv2.dnn.readNetFromONNX(model_path)

# 将图像调整为模型输入尺寸
input_width, input_height = 1024, 512  # 根据模型要求调整
resized_left = cv2.resize(left_undistorted, (input_width, input_height))
resized_right = cv2.resize(right_undistorted, (input_width, input_height))

# 将图像转换为模型输入格式
blob_left = cv2.dnn.blobFromImage(resized_left, scalefactor=1.0, size=(input_width, input_height),
                                  mean=(0, 0, 0), swapRB=False, crop=False)
blob_right = cv2.dnn.blobFromImage(resized_right, scalefactor=1.0, size=(input_width, input_height),
                                   mean=(0, 0, 0), swapRB=False, crop=False)

# 输入模型
net.setInput(blob_left, "left")
net.setInput(blob_right, "right")
disparity = net.forward()

# 将视差图调整为原始图像尺寸
disparity = cv2.resize(disparity[0, 0], (left_undistorted.shape[1], left_undistorted.shape[0]))

# 归一化视差图以便显示
disparity_normalized = cv2.normalize(disparity, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

# 显示视差图
cv2.imshow("Disparity Map", disparity_normalized)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 交互选择点
selected_points = {"left": []}

def select_point(event, x, y, flags, param):
    """鼠标回调函数，用于选择点"""
    if event == cv2.EVENT_LBUTTONDOWN:
        img, img_name = param
        selected_points[img_name].append((x, y))
        print(f"{img_name} 图像选中点: {x, y}")
        # 在图像上标记
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow(f"{img_name.capitalize()} Image", img)

# 显示左图并设置鼠标回调
cv2.imshow("Left Image", left_undistorted)
cv2.setMouseCallback("Left Image", select_point, param=(left_undistorted, "left"))

print("请在左图像上选择两个点（按任意键退出）")
cv2.waitKey(0)
cv2.destroyAllWindows()

if len(selected_points["left"]) != 2:
    print("请在左图像中选择两点！")
    exit()

# 获取选中的点
point1_left, point2_left = selected_points["left"]

# 从视差图中获取视差值
def get_disparity(x, y):
    return disparity[y, x]

disparity1 = get_disparity(point1_left[0], point1_left[1])
disparity2 = get_disparity(point2_left[0], point2_left[1])

if disparity1 > 0 and disparity2 > 0:
    # 计算深度（距离相机的距离）
    depth1 = (mtx_left[0, 0] * baseline) / disparity1
    depth2 = (mtx_left[0, 0] * baseline) / disparity2

    # 转换为 3D 坐标（相机坐标系）
    x1 = (point1_left[0] - mtx_left[0, 2]) * depth1 / mtx_left[0, 0]
    y1 = (point1_left[1] - mtx_left[1, 2]) * depth1 / mtx_left[1, 1]
    z1 = depth1

    x2 = (point2_left[0] - mtx_left[0, 2]) * depth2 / mtx_left[0, 0]
    y2 = (point2_left[1] - mtx_left[1, 2]) * depth2 / mtx_left[1, 1]
    z2 = depth2

    print(f"点1的3D坐标：({x1:.2f}, {y1:.2f}, {z1:.2f})")
    print(f"点2的3D坐标：({x2:.2f}, {y2:.2f}, {z2:.2f})")

    # 计算两点之间的距离
    distance = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
    print(f"两点之间的距离为: {distance:.2f} 米")
else:
    print("视差过小，无法计算深度！")