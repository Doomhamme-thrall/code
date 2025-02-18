import os

import cv2
import numpy as np

calibration_file = "stereo_calibration.npz"
if not os.path.exists(calibration_file):
    print(f"标定文件 {calibration_file} 不存在，请先完成标定！")
    exit()

data = np.load(calibration_file)
mtx_left = data["mtx_left"]
dist_left = data["dist_left"]
mtx_right = data["mtx_right"]
dist_right = data["dist_right"]
R = data["R"]  # 旋转矩阵
T = data["T"]  # 平移向量

# 基线距离（单位：米）
baseline = abs(T[0, 0])

left_image_path = "captured_images/left_002.jpg"
right_image_path = "captured_images/right_002.jpg"


left_image = cv2.imread(left_image_path)
right_image = cv2.imread(right_image_path)

# 校正图像
map_left_1, map_left_2 = cv2.initUndistortRectifyMap(
    mtx_left, dist_left, None, mtx_left, left_image.shape[:2][::-1], cv2.CV_16SC2
)
map_right_1, map_right_2 = cv2.initUndistortRectifyMap(
    mtx_right, dist_right, None, mtx_right, right_image.shape[:2][::-1], cv2.CV_16SC2
)

left_undistorted = cv2.remap(left_image, map_left_1, map_left_2, cv2.INTER_LINEAR)
right_undistorted = cv2.remap(right_image, map_right_1, map_right_2, cv2.INTER_LINEAR)


selected_points = {"left": [], "right": []}


def select_point(event, x, y, flags, param):
    """鼠标回调函数，用于选择点"""
    if event == cv2.EVENT_LBUTTONDOWN:
        img, img_name = param
        selected_points[img_name].append((x, y))
        print(f"{img_name} 图像选中点: {x, y}")
        # 在图像上标记
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow(f"{img_name.capitalize()} Image", img)


cv2.imshow("Left Image", left_undistorted)
cv2.setMouseCallback("Left Image", select_point, param=(left_undistorted, "left"))

cv2.imshow("Right Image", right_undistorted)
cv2.setMouseCallback("Right Image", select_point, param=(right_undistorted, "right"))

print("请在每张图像上选择两个点（按任意键退出）")
cv2.waitKey(0)
cv2.destroyAllWindows()

if len(selected_points["left"]) != 2 or len(selected_points["right"]) != 2:
    print("请在左右图像中各选择两点！")
    exit()

# 计算视差
point1_left, point2_left = selected_points["left"]
point1_right, point2_right = selected_points["right"]

disparity1 = abs(point1_left[0] - point1_right[0])
disparity2 = abs(point2_left[0] - point2_right[0])

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

    # 计算两点间距离
    distance = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)

    print(f"点1的3D坐标：({x1:.2f}, {y1:.2f}, {z1:.2f})")
    print(f"点2的3D坐标：({x2:.2f}, {y2:.2f}, {z2:.2f})")
    print(f"两点之间的距离：{distance * 100:.2f} cm")
else:
    print("视差过小，无法计算深度！")
