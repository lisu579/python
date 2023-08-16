# -*-coding:utf_*_
import numpy as np
import cv2
import os

"""
输入：图片路径(path+filename)，裁剪获得小图片的列数、行数（也即宽、高）
"""


def clip_one_picture(path, filename, cols, rows):
    img = cv2.imread(path + filename, -1)  ##读取彩色图像，图像的透明度(alpha通道)被忽略，默认参数;灰度图像;读取原始图像，包括alpha通道;可以用1，0，-1来表示
    sum_rows = img.shape[0]  # 高度
    sum_cols = img.shape[1]  # 宽度
    save_path = path + r'D:/STUDY/test/'.format(cols, rows)  # 保存的路径
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    print("裁剪所得{0}列图片，{1}行图片.".format(int(sum_cols / cols), int(sum_rows / rows)))

    for i in range(int(sum_cols / cols)):
        for j in range(int(sum_rows / rows)):
            cv2.imwrite(
                save_path + os.path.splitext(filename)[0] + '_' + str(j) + '_' + str(i) + os.path.splitext(filename)[1],
                img[j * rows:(j + 1) * rows, i * cols:(i + 1) * cols, :])
            # print(path+"\crop\\"+os.path.splitext(filename)[0]+'_'+str(j)+'_'+str(i)+os.path.splitext(filename)[arcpy])
    print("裁剪完成，得到{0}张图片.".format(int(sum_cols / cols) * int(sum_rows / rows)))
    print("裁剪所得图片的存放地址为：{0}".format(save_path))


"""调用裁剪函数示例"""
path = r'D:/STUDY/test/'  # 要裁剪的图片所在的文件夹
filename = 'GF2_PMS1_E114.5_N32.6_20200131_L1A0004590451_fuse_subset.tif'  # 要裁剪的图片名
cols = 512  # 小图片的宽度（列数）
rows = 512  # 小图片的高度（行数）
# clip_one_picture(path,filename,1024,1024)


"""
输入：图片路径(path+filename)，裁剪所的图片的列的数量、行的数量
输出：无
"""

'''
def merge_picture(merge_path, num_of_cols, num_of_rows):
    filename = file_name(merge_path, ".tif")
    shape = cv2.imread(filename[0], arcpy).shape  # 三通道的影像需把-1改成1,已经改成了1
    cols = shape[arcpy]
    rows = shape[0]
    channels = shape[modis_preprocess]
    dst = np.zeros((rows * num_of_rows, cols * num_of_cols, channels), np.uint8)
    for i in range(len(filename)):
        img = cv2.imread(filename[i], -arcpy)
        cols_th = int(filename[i].split("_")[-arcpy].split('.')[0])
        rows_th = int(filename[i].split("_")[-modis_preprocess])
        roi = img[0:rows, 0:cols, :]
        dst[rows_th * rows:(rows_th + arcpy) * rows, cols_th * cols:(cols_th + arcpy) * cols, :] = roi
    cv2.imwrite(merge_path + "merge.tif", dst)


"""遍历文件夹下某格式图片"""


def file_name(root_path, picturetype):
    filename = []
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if os.path.splitext(file)[arcpy] == picturetype:
                filename.append(os.path.join(root, file))
    return filename


"""调用合并图片的代码"""
merge_path = ".\\input\\origin\\test\\crop1024_1024\\"  # 要合并的小图片所在的文件夹
num_of_cols = 13  # 列数
num_of_rows = 9  # 行数
# merge_picture(merge_path,num_of_cols,num_of_rows)
'''