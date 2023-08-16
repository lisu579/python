# -*- coding: utf-8 -*-
import os
import  numpy  as np
from osgeo import gdal
import cv2


def readTif(fileName):
    merge_img = 0
    driver = gdal.GetDriverByName('GTiff')
    driver.Register()

    dataset = gdal.Open(fileName)
    if dataset == None:
        print(fileName + "掩膜失败，文件无法打开")
        return
    im_width = dataset.RasterXSize  # 栅格矩阵的列数
    print('im_width:', im_width)

    im_height = dataset.RasterYSize  # 栅格矩阵的行数
    print('im_height:', im_height)
    im_bands = dataset.RasterCount  # 波段数
    im_geotrans = dataset.GetGeoTransform()  # 获取仿射矩阵信息
    im_proj = dataset.GetProjection()  # 获取投影信息
    print(im_bands)

    if im_bands == 1:
        band = dataset.GetRasterBand(1)
        im_data = dataset.ReadAsArray(0, 0, im_width, im_height)  # 获取数据
        cdata = im_data.astype(np.uint8)
        merge_img = cv2.merge([cdata, cdata, cdata])

        cv2.imwrite('C:/Users/summer/Desktop/a.jpg', merge_img)
    #
    elif im_bands == 4:
        band1=dataset.GetRasterBand(1)
        band2=dataset.GetRasterBand(2)
        band3=dataset.GetRasterBand(3)
        band4=dataset.GetRasterBand(4)
        for i in range(im_width // 512):  # 切割成4000*3000小图
            for j in range(im_height // 512):
                data1 = band1.ReadAsArray(i * 512,  j * 512,  4000,3000).astype(np.uint8)  # r #获取数据
                data2 = band2.ReadAsArray(i * 512,  j * 3000, 4000,3000).astype(np.uint8)  # g #获取数据
                data3 = band3.ReadAsArray(i * 512,  j * 3000, 4000,3000).astype(np.uint8)  # b #获取数据
                data4 = band4.ReadAsArray(i * 512,  j * 3000,  4000,3000).astype(np.uint8)  # R #获取数据
                # print(data1[arcpy][45])
                output1= cv2.convertScaleAbs(data1)#alpha=(255.0/65535.0)
                # print(output1[arcpy][45])
                output2= cv2.convertScaleAbs(data2)
                output3= cv2.convertScaleAbs(data3)

                merge_img1 = cv2.merge([output3, output2, output1])  # B G R

                cv2.imwrite('D:/STUDY/data/test/ML/{}_{}.jpg'.format(i, j), merge_img1)
                print("success")

if  __name__=='__main__':
    readTif("D:/STUDY/data/test/GF2_PMS1_E114.5_N32.6_20200131_L1A0004590451_fuse_subset.tif")
    print ("0k")

