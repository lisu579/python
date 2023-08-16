'''
Created on 2020年2月6日
@author: Sun Strong
'''
#coding:utf-8
from osgeo import ogr,osr#osr用于获取坐标系统，ogr用于处理矢量文件
import os
path=r"D:\STUDY\data\GEE\所有变量.csv"
os.chdir(os.path.dirname(path))#将path所在的目录设置为当前文件夹
shp_fn="GF_feature.shp"#即将转化为的shapefile文件名
ds=ogr.Open(path,1)#1代表可读可写，默认为0
csv_lyr=ds.GetLayer()#获取csv文件
sr=osr.SpatialReference()
sr.ImportFromEPSG(4326)#定义坐标系统
shp_driver=ogr.GetDriverByName('ESRI Shapefile')#获取shapefile文件处理句柄
if os.path.exists(shp_fn):#如果文件夹中已存在同名文件则先删除
    shp_driver.DeleteDataSource(shp_fn)
shp_ds=shp_driver.CreateDataSource(shp_fn)
Animal_lyr=shp_ds.CreateLayer(shp_fn,sr,ogr.wkbPoint)#创建一个点图层
tag_id=ogr.FieldDefn('tag_id',ogr.OFTString)#为点图层创建字段
timestamp=ogr.FieldDefn('timestamp',ogr.OFTString)
Animal_lyr.CreateField(tag_id)
Animal_lyr.CreateField(timestamp)
for csv_row in csv_lyr:#对于csv文件中每一行
    point_feature=ogr.Feature(Animal_lyr.GetLayerDefn())#创建一个点
    x=csv_row.GetFieldAsDouble('Lon')#x坐标
    y=csv_row.GetFieldAsDouble('Lat')#y坐标
    shp_pt=ogr.Geometry(ogr.wkbPoint)#创建几何点
    shp_pt.AddPoint(x,y)
    #获取字段值，并写入到该点中
    tag_value=csv_row.GetFieldAsString('individual-local-identifier')
    timestamp_value=csv_row.GetFieldAsString('timestamp')
    point_feature.SetField('tag_id',tag_value)
    point_feature.SetField('timestamp',timestamp_value)
    point_feature.SetGeometry(shp_pt)#将点的几何数据添加到点中
    Animal_lyr.CreateFeature(point_feature)#将点写入到图层中
del ds
del shp_ds#释放句柄，文件缓冲到磁盘
print("This process has succeeded!")
