from osgeo import gdal
import numpy as np
from sklearn import linear_model
import copy

# 计算斜率
def calculate_slope(data):
    reg = linear_model.LinearRegression()
    reg.fit(np.array(range(len(data))).reshape(-1, 1), np.array(data).reshape(-1, 1))
    slope = reg.coef_ # 斜率
    intercept = reg.intercept_ # 截距
    slope = slope[0][0]
    intercept = intercept[0]
    return slope


# 计算变异系数
def coefficient_of_variation(data): # 变异系数
    mean = np.mean(data) # 计算平均值
    std = np.std(data, ddof=0) # 计算标准差
    cv = std/mean
    return cv

# 栅格图像组计算斜率
def slope(images, outpath):
    images_pixels = [] # 存放多个图像像元矩阵的空数组
    for image in images:
        print(f'正在读取栅格图像： {image}')
        tif = str(image)
        open_tif = gdal.Open(tif) # 打开栅格图像
        band = open_tif.GetRasterBand(1).ReadAsArray() # 获取波段的矩阵
        images_pixels.append(band) # 把图像的矩阵加入到数组中
    SLP = copy.deepcopy(images_pixels[0]) # 获取一个矩阵作为要写入的模板
    # 读取像元，并计算变异系数
    print('正在计算')
    for i in range(len(SLP)):
        for j in range(len(SLP[1])):
            if SLP[i][j] >= 0:
                SLP_data = [] # 存放ij坐标下像元值的数组，以计算变异系数
                for px in range(len(images)): # 遍历多个图像下ij坐标的像元值
                    SLP_data.append(images_pixels[px][i][j]) # 同一坐标的多点加入数组，以计算变异系数
                SLP_value = calculate_slope(SLP_data) # 变异系数计算
                SLP[i][j] = SLP_value # 写入该坐标下的变异系数
    print('计算完成')
    # 保存栅格图像
    gtiff_driver = gdal.GetDriverByName('GTiff')
    out_tif = gtiff_driver.Create(outpath, SLP.shape[1], SLP.shape[0], 1, gdal.GDT_Float32)
    # 将数据坐标投影设置为原始坐标投影
    out_tif.SetProjection(open_tif.GetProjection())
    out_tif.SetGeoTransform(open_tif.GetGeoTransform())
    out_band = out_tif.GetRasterBand(1)
    out_band.WriteArray(SLP)
    out_band.FlushCache()
    print('栅格图像组斜率计算完成')

# 栅格图像组计算变异系数
def CV(images, outpath):
    images_pixels = [] # 存放多个图像像元矩阵的空数组
    for image in images:
        tif = str(image)
        open_tif = gdal.Open(tif) # 打开栅格图像
        band = open_tif.GetRasterBand(1).ReadAsArray() # 获取波段的矩阵
        images_pixels.append(band) # 把图像的矩阵加入到数组中
    CV = copy.deepcopy(images_pixels[-1]) # 获取一个矩阵作为要写入的模板
    # 读取像元，并计算变异系数
    for i in range(len(CV)):
        for j in range(len(CV[1])):
            CV_data = [] # 存放ij坐标下像元值的数组，以计算变异系数
            for px in range(len(images)): # 遍历多个图像下ij坐标的像元值
                CV_data.append(images_pixels[px][i][j]) # 同一坐标的多点加入数组，以计算变异系数
            CV_value = coefficient_of_variation(CV_data) # 变异系数计算
            CV[i][j] = CV_value # 写入该坐标下的变异系数
    # 保存栅格图像
    gtiff_driver = gdal.GetDriverByName('GTiff')
    out_tif = gtiff_driver.Create(outpath, CV.shape[1], CV.shape[0], 1, gdal.GDT_Float32)
    # 将数据坐标投影设置为原始坐标投影
    out_tif.SetProjection(open_tif.GetProjection())
    out_tif.SetGeoTransform(open_tif.GetGeoTransform())
    out_band = out_tif.GetRasterBand(1)
    out_band.WriteArray(CV)
    out_band.FlushCache()
    print('栅格图像组变异系数计算完成')


images = [
    r"D:\STUDY\data\MOD16A3\matlab\scale_mod16a3\A2000.tif",
    r"D:\STUDY\data\MOD16A3\matlab\scale_mod16a3\A2001.tif",
    r"D:\STUDY\data\MOD16A3\matlab\scale_mod16a3\A2002.tif",
    r"D:\STUDY\data\MOD16A3\matlab\scale_mod16a3\A2003.tif",
    r"D:\STUDY\data\MOD16A3\matlab\scale_mod16a3\A2004.tif",
    r"D:\STUDY\data\MOD16A3\matlab\scale_mod16a3\A2005.tif",
    r"D:\STUDY\data\MOD16A3\matlab\scale_mod16a3\A2006.tif",
    r"D:\STUDY\data\MOD16A3\matlab\scale_mod16a3\A2007.tif",
    r"D:\STUDY\data\MOD16A3\matlab\scale_mod16a3\A2008.tif",
    r"D:\STUDY\data\MOD16A3\matlab\scale_mod16a3\A2009.tif",
    r"D:\STUDY\data\MOD16A3\matlab\scale_mod16a3\A2010.tif",
    r"D:\STUDY\data\MOD16A3\matlab\scale_mod16a3\A2011.tif",
    r"D:\STUDY\data\MOD16A3\matlab\scale_mod16a3\A2012.tif",
    r"D:\STUDY\data\MOD16A3\matlab\scale_mod16a3\A2013.tif",
    r"D:\STUDY\data\MOD16A3\matlab\scale_mod16a3\A2014.tif",
    r"D:\STUDY\data\MOD16A3\matlab\scale_mod16a3\A2015.tif",
    r"D:\STUDY\data\MOD16A3\matlab\scale_mod16a3\A2016.tif",
    r"D:\STUDY\data\MOD16A3\matlab\scale_mod16a3\A2017.tif",
    r"D:\STUDY\data\MOD16A3\matlab\scale_mod16a3\A2018.tif",
    r"D:\STUDY\data\MOD16A3\matlab\scale_mod16a3\A2019.tif",
    r"D:\STUDY\data\MOD16A3\matlab\scale_mod16a3\A2020.tif",

]

slope(images, r"D:\STUDY\data\MOD16A3\python\slope00_20.tif")
CV(images, r"D:\STUDY\data\MOD16A3\python\cv00_20.tif")
