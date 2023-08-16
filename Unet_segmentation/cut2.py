import os

import cv2
import numpy as np


# 目标分割大小
DES_HEIGHT = 640
DES_WIDTH = 640

# 获取图像信息
path_img = r'G:\A_SCI_DATASET\poppy\voc_wait_cut\img\1modis_preprocess.jpg'

# 获取原始高分辨的图像的属性信息
src = cv2.imread(path_img)
height = src.shape[0]
width = src.shape[1]

# 把原始图像边缘填充至分割大小的整数倍
padding_height = math.ceil(height / DES_HEIGHT) * DES_HEIGHT
padding_width = math.ceil(width / DES_WIDTH) * DES_WIDTH

# 将padding图像与原始图像进行融合，使得原始
padding_img = np.random.randint(0, 255, size=(padding_height, padding_width, 3)).astype(np.uint8)
padding_img[0:height + 0, 0:width + 0] = src

img = padding_img  ##读取彩色图像，图像的透明度(alpha通道)被忽略，默认参数;灰度图像;读取原始图像，包括alpha通道;可以用1，0，-1来表示
sum_rows = img.shape[0]  # 高度
sum_cols = img.shape[1]  # 宽度

cols = DES_WIDTH
rows = DES_HEIGHT

save_path = "crop{0}_{1}\\".format(cols, rows)  # 切割后的照片的存储路径
if not os.path.exists(save_path):
    os.makedirs(save_path)
setDir(save_path)

print("裁剪所得{0}列图片，{1}行图片.".format(int(sum_cols / cols), int(sum_rows / rows)))

filename = os.path.split(path_img)[1]
for i in range(int(sum_cols / cols)):
    for j in range(int(sum_rows / rows)):
        cv2.imwrite(
            save_path + os.path.splitext(filename)[0] + '_' + str(j) + '_' + str(i) + os.path.splitext(filename)[1],
            img[j * rows:(j + 1) * rows, i * cols:(i + 1) * cols, :])
print("裁剪完成，得到{0}张图片.".format(int(sum_cols / cols) * int(sum_rows / rows)))
print("文件保存在{0}".format(save_path))
