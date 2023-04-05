#coding=utf-8
import arcpy
arcpy.CheckOutExtension("spatial")
arcpy.gp.overwriteOutput=1
arcpy.env.workspace = r"D:\STUDY\data\MOD16A3\3"  #输入文件地址
rasters = arcpy.ListRasters("*", "tif")  #遍历栅格文件
mask= r"D:\STUDY\data\MOD16A3\3\xiangjiang\xiangjiang.shp"  #掩磨文件
for raster in rasters:
    print(raster)
    out= r"D:\STUDY\data\MOD16A3\4"+raster #输出文件地址及名称（原名称）
    arcpy.gp.ExtractByMask_sa(raster, mask, out)
    print(raster+"  has done")
    print("All done")