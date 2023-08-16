import numpy as np
import os
import random
from osgeo import gdal
# import cv2
import tifffile as tif
from skimage import data,exposure
from sklearn import preprocessing

#  读取图像像素矩阵
#  fileName 图像文件名
def readTif(fileName):
    dataset = gdal.Open(fileName)
    # width = dataset.RasterXSize
    # height = dataset.RasterYSize
    # GdalImg_data = dataset.ReadAsArray(0, 0, width, height)
    # return GdalImg_data
    return dataset

#保存tif文件函数
def writeTiff(im_data,im_geotrans,im_proj,path):
    if 'int8' in im_data.dtype.name:
        datatype=gdal.GDT_Byte
    elif 'int16' in im_data.dtype.name:
        datatype=gdal.GDT_UInt16
    else:
        datatype=gdal.GDT_Float32
    if len(im_data.shape)==3:
        im_bands,im_height,im_width=im_data.shape
    elif len(im_data.shape)==2:
        im_data=np.array([im_data])
        im_bands,im_height,im_width=im_data.shape
    #创建文件
    driver=gdal.GetDriverByName("GTiff")
    dataset=driver.Create(path,int(im_width),int(im_height),int(im_bands),datatype)
    if(dataset!=None):
        dataset.SetGeoTransform(im_geotrans)#写入仿射变换参数
        dataset.SetProjection(im_proj)#写入投影
    for i in range(im_bands):
        dataset.GetRasterBand(i+1).WriteArray(im_data[i])
    del dataset

def bandsclip(path1,path2):
    dataset_img=readTif(path1)
    width=dataset_img.RasterXSize
    height=dataset_img.RasterYSize
    proj=dataset_img.GetProjection()
    geotrans=dataset_img.GetGeoTransform()
    img=dataset_img.ReadAsArray(0,0,width,height)

    img_out=[]
    #依次将各波段输出
    for i in range(img.shape[0]):
        img_out=np.array(img[i,::])
        #保存tiff格式文件数据
        writeTiff(img_out,geotrans,proj,path2+str(i)+'.tif') #输出波段的名称命名格式可以修改，结合传递的path2参数

os.chdir(r'D:\STUDY\data\bamboo')

path1=r'D:\STUDY\data\bamboo\RF_list.tif'  #要分离波段的原始图像数据名称
path2=r'D:\STUDY\data\bamboo\RF'      #分离的各波段结果图像部分名称
bandsclip(path1,path2)  #调用上面定义的波段分离函数
print('Bandsclip END!')


