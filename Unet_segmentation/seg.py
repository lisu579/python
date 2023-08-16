import gdal
import os


#  批量重采样
def Resample_batch(tifFolder):
    #  获取文件夹内的文件名
    tifNameList = os.listdir(tifFolder)
    for i in range(len(tifNameList)):
        #  判断当前文件是否为tif文件
        if (os.path.splitext(tifNameList[i])[1] == ".tif"):
            tifPath = tifFolder + "/" + tifNameList[i]
            dataset = gdal.Open(tifPath)
            gdal.Warp(os.path.splitext(tifNameList[i])[0] + "_LSTwarp.tif",
                      dataset,
                      width=455,
                      height=443,
                      cutlineDSName=r"E:\Remote_Sensing_Data\TVDI\mask\mask.shp",
                      cropToCutline=True)
            print(os.path.splitext(tifNameList[i])[0] + "_warp.tif wraoed successfully!")


Resample_batch(r"E:\Remote_Sensing_Data\TVDI\MOD11A2\2012tif")