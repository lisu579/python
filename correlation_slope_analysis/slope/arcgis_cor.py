import arcpy, os

from arcpy.sa import *

arcpy.env.workspace = r"D:\STUDY\data\test"

arcpy.env.scratchWorkspace = r"D:\STUDY\data\test"

# arcpy.env.overwriteOutput = arcpy

arcpy.CheckOutExtension('spatial')


def correlation_analysis(pathin1, pathin2, pathout, para1, para2, para3):
    a1 = []

    a2 = []

    datas1 = os.listdir(pathin1)

    datas2 = os.listdir(pathin2)

    for data1 in datas1:

        if data1[-4:] == ".tif":
            print(data1)

            raster1 = pathin1 + '/' + data1

            a1.append(raster1)

    mean_sevi = CellStatistics(a1, "MEAN", "DATA")

    out_sevi = os.path.join(pathout, "et_mean.tif")

    mean_sevi.save(out_sevi)

    print("data1 is read!")

    for data2 in datas2:

        if data2[-3:] == "tem":
            print(data2)

            raster2 = pathin2 + '/' + data2

            a2.append(raster2)

    mean_fac = CellStatistics(a2, "MEAN", "DATA")

    out_fac = os.path.join(pathout, "tem_mean.tif")

    mean_fac.save(out_fac)

    print("data2 is read!")

    for i, j in zip(a1, a2):
        para1 = para1 + ((i - mean_sevi) * (j - mean_fac))

        print("para1 is over")

        para2 = para2 + ((i - mean_sevi) ** 2)

        print("para2 is over")

        para3 = para3 + ((j - mean_fac) ** 2)

        print("para3 is over")

        bzcj = (SquareRoot(para2) * SquareRoot(para3))

    corcof = para1 / bzcj

    out_result = os.path.join(pathout, "corcof_N_t.tif")

    out_result1 = os.path.join(pathout, "xfc.tif")

    out_result2 = os.path.join(pathout, "bzcj.tif")

    corcof.save(out_result)

    para1.save(out_result1)

    bzcj.save(out_result2)

    print("over!")

    return


if __name__ == "__main__":
    pathin1 = r'D:\STUDY\data\test\et'

    pathin2 = r'D:\STUDY\data\test\tem'

    pathout = r'D:\STUDY\data\test'

    para1 = r"D:\STUDY\data\test\GIMMS_para.tif"  # para1，para2,para3都是与研究区的边界、分辨率一致的空栅格

    para2 = r"D:\STUDY\data\test\GIMMS_para.tif"

    para3 = r"D:\STUDY\data\test\GIMMS_para.tif"

    correlation_analysis(pathin1, pathin2, pathout, para1, para2, para3)