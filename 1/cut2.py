from osgeo import gdal
import os


tifFolder = r'D:\STUDY\data\MOD16A3\3'
saveFolder = r'D:\STUDY\data\MOD16A3\4'
input_shape = r'D:\STUDY\data\SHP\xiangjiang\xiangjiang.shp'  # or any other format


tifNameList = os.listdir(tifFolder)

for i in range(len(tifNameList)):

    filename, txt = os.path.splitext(tifNameList[i])

    if txt == '.tif':
        tifPath = tifFolder + os.sep + tifNameList[i]
        outName = saveFolder + os.sep + filename + '_cut' + txt
        ds = gdal.Warp(outName,
                       tifPath,
                       format='GTiff',
                       cutlineDSName=input_shape,  # or any other file format
                       # cutlineWhere="FIELD = 'whatever'"
                       # optionally you can filter your cutline (shapefile) based on attribute values
                       dstNodata=65534)  # select the no data value you like
        '''ds = None  # do other stuff with ds object, it is your cropped dataset. 
        in this case we only close the dataset.'''
        print('{filename} deal end '.format(filename=outName))
        del ds
