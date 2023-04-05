'''from osgeo import gdal

outputfilePath = r'D:\STUDY\data\MOD13A1\2000\2'
inputrasfile1 = r'D:\STUDY\data\MOD13A1\2000\1\MOD13A1.A2000049.h27v06.006.2015136104712.hdf'
inputrasfile2 = r'D:\STUDY\data\MOD13A1\2000\1\MOD13A1.A2000049.h28v06.006.2015136104712.hdf'

gdal.Warp(outputfilePath,[inputrasfile1,inputrasfile2])'''
# 如果图片大于4G，需要在输入图片路径前加入 -co BIGTIFF=YES
import subprocess
import os

create_slope = '''D:/python/python.exe D:/python/Scripts/gdal_merge.py -of GTiff -o '''
list = []
fileDir = 'D:\STUDY\data\MOD13A1\2000\1'
filepath = os.listdir(fileDir)
for f in filepath:
    s = (fileDir + "/" + f)
    list.append(s)
print(list)
tarDir = r'D:\STUDY\data\MOD13A1\2000\2'
filename = ' '.join(list)
print(filename)

subprocess.call(create_slope + r'D:\STUDY\data\MOD13A1\2000\1\MOD13A1.A2000049.h27v06.006.2015136104712.hdf' + ' ' + '-co COMPRESS=LZW ' + filename)



