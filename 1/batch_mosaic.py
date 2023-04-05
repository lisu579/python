##arcpy的批量拼接
#!/usr/bin/python
# -*- coding: UTF-8 -*-


import os
import arcpy
import time


def show_files(path, out_files, suffix=".tif", out_type="path"):
    file_list = os.listdir(path)
    for file in file_list:
        cur_path = os.path.join(path, file)
        if os.path.isdir(cur_path):
            show_files(cur_path, out_files, out_type=out_type)
        else:
            if file.endswith(suffix):
                if out_type == "path":
                    out_files.append(cur_path)
                elif out_type == "name":
                    out_files.append(file)
                else:
                    raise Exception("please select correct out_type value：path ；name")


in_path = arcpy.GetParameterAsText(0)
out_path = arcpy.GetParameterAsText(1)
pixel_type = arcpy.GetParameterAsText(2)
mosaic_method = arcpy.GetParameterAsText(3)
colormap_mode = arcpy.GetParameterAsText(4)

all_tifs = []
groups = {}
show_files(in_path, all_tifs, out_type="name")
arcpy.env.workspace = in_path

base = all_tifs[0]
out_coor_system = arcpy.Describe(base).spatialReference
cell_width = arcpy.Describe(base).meanCellWidth
band_count = arcpy.Describe(base).bandCount

for i in all_tifs:
    filename = i
    k = '.'.join(filename.split('.')[:2]) + '.' + '.'.join(filename.split('.')[-2:])
    if k in groups:
        groups[k].append(i)
    else:
        groups[k] = []
        groups[k].append(i)

nums = len(groups)
num = 1
for i in groups:
    s = time.time()
    groups[i] = ';'.join(groups[i])
    if not os.path.exists(os.path.join(out_path, i)):
        arcpy.MosaicToNewRaster_management(groups[i], out_path, i, out_coor_system, pixel_type, cell_width, band_count, mosaic_method, colormap_mode)
        e = time.time()
        arcpy.AddMessage("{0}/{1} | {2} Completed, time used {3}s".format(num, nums, i, e-s))
    else:
        e = time.time()
        arcpy.AddMessage("{0}/{1} | {2} existed, , time used {3}s".format(num, nums, i, e-s))
    num = num + 1
