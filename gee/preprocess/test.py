
nums = len(groups)
num = 1
for i in groups:
    s = time.time()
    month = int(i.split(".")[0][6:])  # A2000M2.tif
    if len(groups[i]) == 0:
        arcpy.AddMessage("{0}/{1} | {2} is None".format(num, nums, i))
        num = num + 1
        continue
    groups[i] = ';'.join(groups[i])
    if not os.path.exists(os.path.join(out_path, i)):
        if month != 12:
            arcpy.MosaicToNewRaster_management(groups[i], out_path, i, out_coor_system, pixel_type, cell_width,
                                               band_count,
                                               "MEAN", colormap_mode)
        else:
            arcpy.MosaicToNewRaster_management(groups[i], out_path, i, out_coor_system, pixel_type, cell_width,
                                               band_count,
                                               "SUM", colormap_mode)
        e = time.time()
        arcpy.AddMessage("{0}/{1} | {2} Completed, time used {3}s".format(num, nums, i, e - s))
    else:
        e = time.time()
        arcpy.AddMessage("{0}/{1} | {2} existed, , time used {3}s".format(num, nums, i, e - s))
    num = num + 1