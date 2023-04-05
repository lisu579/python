from osgeo import gdal, osr
from osgeo import gdal_array
import os
import time
import numpy as np
start = time.time()
'''
第一个函数:批量读取文件夹中hdf格式的modis产品数据并进行几何校正(WGS84)
'''


def readHdfWithGeo(hdfFloder, saveFloder):
    # 获取输入文件夹中所有的文件名
    hdfNameList = os.listdir(hdfFloder)
    # 遍历文件名列表中所有文件
    for i in range(len(hdfNameList)):
        # 获取文件名后缀
        dirname, basename = os.path.split(hdfNameList[i])
        filename, txt = os.path.splitext(basename)
        # 判断文件后缀是否为 .hdf
        if txt == '.hdf':
            hdfPath = hdfFloder + os.sep + hdfNameList[i]
            # 打开hdf文件
            datasets = gdal.Open(hdfPath)
            # 打开子数据集
            dsSubDatasets = datasets.GetSubDatasets()
            # 打开ndvi数据
            ndviRaster = gdal.Open(dsSubDatasets[0][0])
            # 获取元数据
            metaData = datasets.GetMetadata()
            # for key, value in metaData.items():
            #   print('{key}:{value}'.format(key = key, value = value))
            # 获取数据时间
            time = metaData['RANGEBEGINNINGDATE']
            #获取带号
            tile = metaData['HORIZONTALTILENUMBER']
            # 命名输出完整路径文件名
            outName = saveFloder + os.sep + time + tile + '.tif'
            # 进行几何校正
            geoData = gdal.Warp(outName, ndviRaster,
                                dstSRS='EPSG:4326', format='GTiff',
                                resampleAlg=gdal.GRA_Bilinear)
            del geoData
            print('{outname} deal end'.format(outname=outName))


start = time.time()

readHdfWithGeo(r'D:\STUDY\data\MOD13A1\2000\1',r'D:\STUDY\data\MOD13A1\2000\2')
end = time.time()
print('deal spend: {s} s'.format(s=end - start))