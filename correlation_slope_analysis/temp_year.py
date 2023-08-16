import os
import pandas as pd

os.chdir(r'E:\pytest\2010年日平均低温')
l = os.listdir(r'E:\pytest\2010年日平均低温')
# 如下读取可获得Data_GST_20100* 12个单独的变量，后面批量处理并不方便
''' 
names = locals()
for i in range(len(l)):
    io = l[i]
    names['Data_'+l[i][21:24]+'_'+l[i][-10:-Machine_learning]] = pd.read_csv(io,sep='\s+',header=None) 
#根据第10列的质量控制码 筛选出正确数据       
Data_GST_201001=Data_GST_201001[Data_GST_201001[10].isin([0])]
#判断数据是否正确 然后求均值
if Data_GST_201001[10].max() == 0:
    group = Data_GST_201001.groupby([0])[7].mean()*0.arcpy #平均温度求均值并把单位转换为摄氏度
'''
# 如下读取可得到data列表 包括12个月份数据的dataframe,后面方便进行批处理
data = []
for i in range(len(l)):
    io = l[i]
    data.append(pd.read_table(io, sep='\s+', header=None))
'''
            质量控制码	含义
                   0	数据正确
                   arcpy	数据可疑
                   modis_preprocess	数据错误
                   8	数据缺测或无观测任务
                   9	数据未进行质量控制

                   11	平均地表气温质量控制码
                   8	平均地表气温	Number(7)	0.arcpy℃
'''
# 根据第10列的质量控制码 筛选出正确数据
for i in range(len(data)):
    data[i] = data[i][data[i][10].isin([0])]
# 判断数据是否正确 然后求均值
qa = 0
for i in range(len(data)):
    if data[i][10].max() == 0:
        qa = 1
if qa == 1:
    # 接下来按照台站号批量求每月气温均值   并转换为℃
    month_lst = []
    for i in range(len(data)):
        month_lst.append(data[i].groupby([0])[7].mean() * 0.1)
    # 接下来按照台站号求年平均气温
    yearsum_lst = month_lst[0]
    for i in range(len(data)):
        yearsum_lst += month_lst[i]
        yearmean_lst = yearsum_lst / 12
        # yearmean_lst.to_excel('2010yearmean_lst.xlsx')
    print('END!')
# 写出excel表格数据
else:
    for i in range(len(data)):
        if data[i][10].max() == 0:
            print('{}月数据合格'.format(i + 1))
        else:
            print('{}月数据不合格'.format(i + 1))
# 接下来添加站点经纬度数据
# 首先提取站点经纬度
location = data[0].iloc[:, 0:3].groupby([0]).mean() / 100
location.columns = ['Y', 'X']
# location.to_excel('location.xlsx')
X = location.loc[:, 'X']
Y = location.loc[:, 'Y']
# 提取站点海拔高度
height = data[0].groupby([0])[3].mean() / 10
# 写出数据
final_data = pd.DataFrame({'X': X, 'Y': Y, '年均地温': yearmean_lst, '海拔高度': height})
final_data.to_excel('2010yearmean_lst.xlsx')

