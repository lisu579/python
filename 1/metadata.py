from osgeo import gdal
import os
import glob

#  gdal打开hdf数据集
os.chdir(r'D:\STUDY\data\MOD13A1\2000\1')
file_list = glob.glob("*.hdf")
for i in file_list:
    datasets = gdal.Open(i)
    #  获取hdf中的子数据集
    SubDatasets = datasets.GetSubDatasets()
    Metadata = datasets.GetMetadata()
    #  打印元数据
    for key,value in Metadata.items():
        print('{key}:{value}'.format(key = key, value = value))
    #  获取要转换的子数据集
    data = datasets.GetSubDatasets()[0][0]
    Raster_DATA = gdal.Open(data)
    DATA_Array = Raster_DATA.ReadAsArray()
    print(DATA_Array)
    #  保存为tif
    TifName = r'D:\STUDY\data\MOD13A1\2000\2'
    geoData = gdal.Warp(TifName, Raster_DATA,
                    dstSRS = 'EPSG:4326', format = 'GTiff',
                    resampleAlg = gdal.GRA_Bilinear)
    del geoData