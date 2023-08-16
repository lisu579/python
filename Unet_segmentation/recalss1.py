import gdal
import os


#  批量重采样
def Resample_batch(tifFolder):
    #  获取文件夹内的文件名
    tifNameList = os.listdir(tifFolder)
    for i in range(len(tifNameList)):
        #  判断当前文件是否为tif文件
        if (os.path.splitext(tifNameList[i])[1] == ".tiff"):
            tifPath = tifFolder + "/" + tifNameList[i]
            dataset = gdal.Open(tifPath)
            gdal.Warp(os.path.splitext(tifNameList[i])[0] + "_re.tif",
                      dataset,
                      width=1024,
                      height=1024)
            print(os.path.splitext(tifNameList[i])[0] + "_re.tif wrapped successfully!")


Resample_batch(r"D:\STUDY\data\road\test\input")