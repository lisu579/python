from osgeo import gdal
import time
import numpy as np
start = time.time()

#第三个函数:写出tif文件
'''
def read_tif(filename):
    dataset=gdal.Open(filename)

    im_width = dataset.RasterXSize
    im_height = dataset.RasterYSize

    im_geotrans = dataset.GetGeoTransform()
    im_proj = dataset.GetProjection()
    im_data = dataset.ReadAsArray(0,0,im_width,im_height)

    del dataset 
    return im_proj,im_geotrans,im_width, im_height,im_data

'''
#保存tif
def writeTiff(im_data, nan, im_geotrans, im_proj, path):
    if 'int8' in im_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in im_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32

    if len(im_data.shape) == 3:
        im_bands, im_height, im_width = im_data.shape
    elif len(im_data.shape) == 2:
        im_data = np.array([im_data])
        im_bands, im_height, im_width = im_data.shape

    # 创建文件
    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(path, int(im_width), int(im_height), int(im_bands), datatype)

    if (dataset != None):
        dataset.SetGeoTransform(im_geotrans)  # 写入仿射变换参数
        dataset.SetProjection(im_proj)  # 写入投影

    if im_bands == 1:
        dataset.GetRasterBand(1).WriteArray(im_data)
    else:
        for i in range(im_bands):
            dataset.GetRasterBand(i + 1).WriteArray(im_data[i])
            outBand = dataset.GetRasterBand(i + 1)
            outBand.FlushCache()
            outBand.SetNoDataValue(nan)
    del dataset


'''
# -*- coding: utf-8 -*-
import os
import gdal
import numpy as np
from skimage import morphology,filters

def read_img(filename):
    dataset=gdal.Open(filename)

    im_width = dataset.RasterXSize
    im_height = dataset.RasterYSize

    im_geotrans = dataset.GetGeoTransform()
    im_proj = dataset.GetProjection()
    im_data = dataset.ReadAsArray(0,0,im_width,im_height)

    del dataset 
    return im_proj,im_geotrans,im_width, im_height,im_data


def write_img(filename, im_proj, im_geotrans, im_data):
    if 'int8' in im_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in im_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32

    if len(im_data.shape) == 3:
        im_bands, im_height, im_width = im_data.shape
    else:
        im_bands, (im_height, im_width) = 1,im_data.shape 

    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(filename, im_width, im_height, im_bands, datatype)

    dataset.SetGeoTransform(im_geotrans)
    dataset.SetProjection(im_proj)

    if im_bands == 1:
        dataset.GetRasterBand(1).WriteArray(im_data)
    else:
        for i in range(im_bands):
            dataset.GetRasterBand(i+1).WriteArray(im_data[i])

    del dataset

if __name__ == '__main__':
    path = 'D:/0220/sample/'
    out = 'D:/0220/temp/'
    fs = os.listdir(path)
    for f in fs:
        if f[-4:] == '.tif':
            f_path = os.path.join(path, f)
            im_proj,im_geotrans,im_width, im_height,im_data = read_img(f_path)
            temp = np.zeros((3,im_data.shape[1],im_data.shape[2])) #取3个波段
            temp[0,...] = im_data[0,...]
            temp[1,...] = im_data[1,...]
            temp[2,...] = im_data[2,...]
            out_path = os.path.join(out, f)
            write_img(out_path, im_proj, im_geotrans, temp)
'''