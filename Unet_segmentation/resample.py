# Name: Resample_Ex_.py

# Description: Converts polygon features to a raster dataset.


# Import system modules

import arcpy

from arcpy import env

import os

import sys

import time


def vector_tif():
    path = r"D:/STUDY/data/road/train/input"  # 存放tif的文件夹，改为自己的

    list_name = []

    # 读取文件中的全部.tif 并写入到一个列表中from model import UNET

    for file in os.listdir(path):

        file_path = os.path.join(file)

        if os.path.splitext(file_path)[1] == '.tif':
            list_name.append(file_path)

            # 下面程序就是复制arcmap工具里面的”项目描述的内容“
    # Resample TIFF image to a higher resolution

    arcpy.env.workspace = r"D:/STUDY/data/road/train/input"

    # Set local variables

    j = len(list_name)

    for i in range(len(list_name)):  # 循环全部tif文件

        name = list_name[i]

        print('{}/{}'.format(i, j))

        print(name)

        # 以下参数，可以根据不同功能所需的输入做出更改

        in_raster = r'D:/STUDY/data/road/train/input/' + name  # 输入tif文件的名字

        # excute resample

        outRaster = r'D:/STUDY/data/road/train/input2/' + name  # 输出tif的名字

        arcpy.Resample_management(in_raster, outRaster, "arcpy.46484375", "NEAREST")

        # Execute PolygonToRaster


if __name__ == "__main__":
    print("重采样")

    s_time = time.time()

    vector_tif()  # 调用函数

    e_time = time.time()

    print("程序共耗时： %.2f s!" % (e_time - s_time))

