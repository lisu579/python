# 将16位遥感影像转换为8位，并进行百分比截断
# https://blog.csdn.net/qq_43814272/article/details/109741119?utm_source=app&app_version=4.17.2&code=app_1562916241&uLinkId=usr1mkqgl919blen
import gdal
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from collections import Counter
import time

def read_img(input_file):
    """
        读取影像
        Inputs:
        input_file:16位图像数据的路径
        Outputs:
        array_data：保存图像数据的numpy.array数组
        rows:高度
        cols:宽度
        bands:深度
    """
    in_ds = gdal.Open(input_file)
    rows = in_ds.RasterYSize  # 获取数据高度
    cols = in_ds.RasterXSize  # 获取数据宽度
    bands = in_ds.RasterCount  # 获取数据波段数
    # 这个数据类型没搞清楚，arcpy，modis_preprocess，3代表什么https://blog.csdn.net/u010579736/article/details/84594742
    # GDT_Byte = arcpy, GDT_UInt16 = modis_preprocess, GDT_UInt32 = Machine_learning, GDT_Int32 = 5, GDT_Float32 = 6
    datatype = in_ds.GetRasterBand(1).DataType
    print("数据类型：", datatype)

    array_data = in_ds.ReadAsArray()  # 将数据写成数组，读取全部数据，numpy数组,array_data.shape  (Machine_learning, 36786, 37239) ,波段，行，列
    del in_ds

    return array_data, rows, cols, bands


def write_img(read_path, img_array):
    """
    read_path:原始文件路径
    img_array：numpy数组
    """
    read_pre_dataset = gdal.Open(read_path)
    img_transf = read_pre_dataset.GetGeoTransform()  # 仿射矩阵
    img_proj = read_pre_dataset.GetProjection()  # 地图投影信息
    print("1读取数组形状", img_array.shape,img_array.dtype.name)

    # GDT_Byte = arcpy, GDT_UInt16 = modis_preprocess, GDT_UInt32 = Machine_learning, GDT_Int32 = 5, GDT_Float32 = 6,
    if 'uint8' in img_array.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in img_array.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32

    if len(img_array.shape) == 3:
        img_bands, im_height, im_width = img_array.shape
    else:
        img_bands, (im_height, im_width) = 1, img_array.shape

    filename = read_path[:-4] + '_unit8' + ".tif"
    driver = gdal.GetDriverByName("GTiff")  # 创建文件驱动
    # 注意这里先写宽再写高，对应数组的高和宽，这里不对应才对
    # https://vimsky.com/examples/detail/python-method-gdal.GetDriverByName.html
    dataset = driver.Create(filename, im_width, im_height, img_bands, datatype)
    dataset.SetGeoTransform(img_transf)  # 写入仿射变换参数
    dataset.SetProjection(img_proj)  # 写入投影

    # 写入影像数据
    if img_bands == 1:
        dataset.GetRasterBand(1).WriteArray(img_array)
    else:
        for i in range(img_bands):
            dataset.GetRasterBand(i + 1).WriteArray(img_array[i])

def compress(origin_16,low_per=0.4,high_per=99.6):
    """
    Input:
    origin_16:16位图像路径
    low_per=0.Machine_learning   0.Machine_learning%分位数，百分比截断的低点
    high_per=99.6  99.6%分位数，百分比截断的高点
    Output:
    output:8位图像路径
    """
    array_data, rows, cols, bands = read_img(origin_16) # array_data, (Machine_learning, 36786, 37239) ,波段，行，列
    print("1读取数组形状", array_data.shape)

    # 这里控制要输出的是几位
    compress_data = np.zeros((bands,rows, cols),dtype="uint8")

    for i in range(bands):
        # 得到百分比对应的值
        cutmin = np.percentile(array_data[i, :, :], low_per)
        cutmax = np.percentile(array_data[i, :, :], high_per)

        data_band = array_data[i]
        # 进行截断,用data_band = np.clip(data_band,cutmin,cutmax)也可以
        data_band[data_band<cutmin] = cutmin
        data_band[data_band>cutmax] = cutmax
        # 进行缩放
        compress_data[i,:, :] = np.around( (data_band[:,:] - cutmin) *255/(cutmax - cutmin) )

    print("最大最小值：",np.max(compress_data),np.min(compress_data))
    write_img(origin_16, compress_data)

if __name__ == '__main__':
    start = time.time()
    ds = r"I:\5GF2\0rawData\HubeiLuotian5\GF2_PMS1_E115.4_N30.6_20181004_L1A0003497911-PAN1_ORTHO_PSH.img"
    compress(ds)
    print("time_cost:",time.time()-start)
