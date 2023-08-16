from osgeo import gdal
import os
"""
多个单波段tif合并成一个tif文件
"""
#修改路径
tifDir = r"D:\STUDY\data\meteology\hunan\tem"  #tif路径 单波段
outtif = r"D:\STUDY\data\meteology\hunan\tem\tem.tif"

NP2GDAL_CONVERSION = {
  "uint8": 1,
  "int8": 1,
  "uint16": 2,
  "int16": 3,
  "uint32": 4,
  "int32": 5,
  "float32": 6,
  "float64": 7,
  "complex64": 10,
  "complex128": 11,
}
tifs = [i for i in os.listdir(tifDir) if i.endswith(".tif")]
#获取投影波段数等信息
bandsNum = len(tifs)
dataset = gdal.Open(os.path.join(tifDir,tifs[0]))
projinfo = dataset.GetProjection()
geotransform = dataset.GetGeoTransform()
cols,rows=dataset.RasterXSize,dataset.RasterYSize
datatype=dataset.GetRasterBand(1).ReadAsArray(0,0,1,1).dtype.name
gdaltype=NP2GDAL_CONVERSION[datatype]
dataset=None
#创建目标文件
format = "GTiff" #tif格式
#format = "ENVI"  # ENVI格式
driver = gdal.GetDriverByName(format)
dst_ds = driver.Create(outtif,cols, rows,bandsNum, gdaltype,options=['COMPRESS=LZW'])
dst_ds.SetGeoTransform(geotransform)
dst_ds.SetProjection(projinfo)
#写入文件
info = set()
for k in range(bandsNum):
    ds = gdal.Open(os.path.join(tifDir,tifs[k]))
    X,Y = ds.RasterXSize,ds.RasterYSize
    info.add("%s,%s"%(X,Y))
    if(len(info) != 1):
        dst_ds = None
        ds = None
        print("%s 列数行数不一样：%s,%s"%(tifs[k],X,Y))
        raise Exception("有影像行列数不一致")
    data = ds.GetRasterBand(1).ReadAsArray()    ##读取第一波段
    ds = None
    dst_ds.GetRasterBand(k+1).WriteArray(data)
    dst_ds.GetRasterBand(k+1).SetDescription("hahha_%s"%k)
    print("波段 %s ==> 文件 %s"%(k+1,tifs[k]))
dst_ds = None