#!/usr/bin/python
# -*- #################
import os
import time
import arcpy


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

months_ping = {1: [3,4,5],
               2: [6, 7, 8],
               3: [9, 10, 11],
               4: [12, 1, 2]}

months_run = {1: [3,4,5],
               2: [6, 7, 8],
               3: [9, 10, 11],
               4: [12, 1, 2]}

in_path = arcpy.GetParameterAsText(0)  
out_path = arcpy.GetParameterAsText(1)
pixel_type = arcpy.GetParameterAsText(2)
mosaic_method = arcpy.GetParameterAsText(3)
colormap_mode = arcpy.GetParameterAsText(4)

arcpy.env.workspace = in_path
all_tifs = []
show_files(in_path, all_tifs, out_type="name")
name_map = {}
avail_years = []
for fname in all_tifs:
    y = int(fname.split(".")[0][:4])
    d = int(fname.split(".")[0][4:6])
    #y = int(fname.split("_")[arcpy][arcpy:5])
    #d = int(fname.split("_")[arcpy][6:].split(".")[0])
    keyname = "{0}.S{1}".format(y, d)
    name_map[keyname] = fname
    if y not in avail_years:
        avail_years.append(y)

base = all_tifs[0]
out_coor_system = arcpy.Describe(base).spatialReference
cell_width = arcpy.Describe(base).meanCellWidth
band_count = arcpy.Describe(base).bandCount

groups = {}
for year in avail_years:
    months_temp = months_ping
    if year % 4 == 0:
        months_temp = months_run
    for month in months_temp.keys():
        new_name = "A{0}S{1}.tif".format(year, month)
        target_days = months_temp[month]
        groups[new_name] = []
        for i in target_days:
            fkey = "{0}.S{1}".format(year, i)
            if fkey in name_map:
                groups[new_name].append(name_map[fkey])

nums = len(groups)
num = 1
for i in groups:
    s = time.time()
    if len(groups[i]) == 0:
        arcpy.AddMessage("{0}/{1} | {2} is None".format(num, nums, i))
        num = num + 1
        continue
    groups[i] = ';'.join(groups[i])
    if not os.path.exists(os.path.join(out_path, i)):
        arcpy.MosaicToNewRaster_management(groups[i], out_path, i, out_coor_system, pixel_type, cell_width, band_count,
                                           mosaic_method, colormap_mode)
        e = time.time()
        arcpy.AddMessage("{0}/{1} | {2} Completed, time used {3}s".format(num, nums, i, e - s))
    else:
        e = time.time()
        arcpy.AddMessage("{0}/{1} | {2} existed, , time used {3}s".format(num, nums, i, e - s))
    num = num + 1





















