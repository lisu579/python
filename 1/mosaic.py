from osgeo import gdal

outputfilePath = r'D:\STUDY\data\MOD13A1\2000\2'
inputrasfile1 = r'D:\STUDY\data\MOD13A1\2000\1\MOD13A1.A2000049.h27v06.006.2015136104712.hdf'
inputrasfile2 = r'D:\STUDY\data\MOD13A1\2000\1\MOD13A1.A2000049.h28v06.006.2015136104712.hdf'

gdal.Warp(outputfilePath,[inputrasfile1,inputrasfile2])



