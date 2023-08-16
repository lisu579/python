import numpy as np
from osgeo import gdal
import time



def compute(arr1, arr2, src_nodta):
    """
    计算相关系数，c为通道数，h为行数，w为列数
    :param arr1: 影像1的数据，np数组，shape为[c,h,w]
    :param arr2: 影像2的数据，np数组，shape为[c,h,w]
    :param src_nodta: 忽略值，数字
    :return: 相关系数图像，np数组，shape为[h,w]
    """
    band1 = arr1[0]
    out = band1 * 0 - 2222
    rows, colmns = out.shape
    for row in range(rows):
        for col in range(colmns):
            if src_nodta is None:
                x1 = arr1[:, row, col]
                x2 = arr2[:, row, col]
                corr = np.corrcoef(x1, x2)[0, 1]
                out[row, col] = corr
            else:
                if band1[row, col] != src_nodta:
                    x1 = arr1[:, row, col]
                    x2 = arr2[:, row, col]
                    corr = np.corrcoef(x1, x2)[0, 1]
                    out[row, col] = corr
    return out

def yiyuanhuigui(imgpath1, imgpath2, outtif):
    """
    计算两个影像的相关系数
    :param imgpath1: 影像1，多波段
    :param imgpath2: 影像2，与影像1的波段数相同、行列数相同
    :param outtif: 输出结果路径
    :return: None
    """
    # 读取影像1的信息和数据
    ds1 = gdal.Open(imgpath1)
    projinfo = ds1.GetProjection()
    geotransform = ds1.GetGeoTransform()
    rows = ds1.RasterYSize
    colmns = ds1.RasterXSize
    data1 = ds1.ReadAsArray()
    print(data1.shape)
    # 读取影像2的数据
    ds2 = gdal.Open(imgpath2)
    data2 = ds2.ReadAsArray()
    src_nodta = ds1.GetRasterBand(1).GetNoDataValue()

    # 创建输出图像
    format = "GTiff"
    driver = gdal.GetDriverByName(format)
    dst_ds = driver.Create(outtif, colmns, rows, 1, gdal.GDT_Float32)
    dst_ds.SetGeoTransform(geotransform)
    dst_ds.SetProjection(projinfo)

    # 删除对象
    ds1 = None
    ds2 = None

    # 开始计算相关系数
    out = compute(data1, data2, src_nodta)
    # 写出图像
    dst_ds.GetRasterBand(1).WriteArray(out)

    # 设置nodata
    dst_ds.GetRasterBand(1).SetNoDataValue(-2222)
    dst_ds = None

if __name__ == "__main__":
    tif1 = r"D:\STUDY\data\MOD16A3\mean\mean_2000_20.tif"
    tif2 = r"D:\STUDY\data\MOD16A3\mean\TEM.tif"
    outtif = r"D:\STUDY\data\MOD16A3\mean\cor_ET_TEM.tif"
    t0 = time.time()
    yiyuanhuigui(tif1, tif2, outtif)
    print(time.time() - t0)
