from osgeo import gdal, osr
import os
import time

start = time.time()


'''第五个函数:批量进行重投影'''


def reproject(tifFolder, saveFolder, proj4):
    tifNameList = os.listdir(tifFolder)

    srs = osr.SpatialReference()
    srs.ImportFromProj4(proj4)

    for i in range(len(tifNameList)):

        filename, txt = os.path.splitext(tifNameList[i])
#？？？？？？？待解决问题：xRes是否为像素大小?这里把1000改成500(失败)→改回1000
        if txt == '.tif':
            tifPath = tifFolder + os.sep + tifNameList[i]
            outName = saveFolder + os.sep + filename + '_rep' + txt
            reproData = gdal.Warp(outName, tifPath, dstSRS=srs,
                                  xRes=1000, yRes=1000,
                                  resampleAlg=gdal.GRA_Bilinear,
                                  outputType=gdal.GDT_Float32)
            print('{filename} deal end '.format(filename=outName))
            del reproData

#记得修改文件夹路径
start = time.time()
reproject(r'D:\STUDY\data\MOD16A3\5_mosaic',
          r'D:\STUDY\data\MOD16A3\4_proj',
          '+proj=aea +lat_0=0 +lon_0=112 +lat_1=27 +lat_2=28 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs')
end = time.time()
print('deal spend: {s} s'.format(s=end - start))
