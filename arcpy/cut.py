from osgeo import gdal, osr
from osgeo import gdal_array
import os
import time
import numpy as np

start = time.time()

def cut(tifFolder, saveFolder, shpFile):
    tifNameList = os.listdir(tifFolder)

    for i in range(len(tifNameList)):

        filename, txt = os.path.splitext(tifNameList[i])

        if txt == '.tif':
            tifPath = tifFolder + os.sep + tifNameList[i]
            outName = saveFolder + os.sep + filename + '_cut' + txt
            cut_ds = gdal.Warp(outName, tifPath,
                    cutlineDSName=shpFile,
                    cropToCutline=True)
            print('{filename} deal end '.format(filename=outName))
            del cut_ds

start = time.time()
cut(r'D:\STUDY\data\MOD13A1\2000\6_mosaic',
    r'D:\STUDY\data\MOD13A1\2000\5_cut',
    r'D:\STUDY\data\SHP\albers\albers.shp')
end = time.time()
print('deal spend: {s} s'.format(s=end - start))
