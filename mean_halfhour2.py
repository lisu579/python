import csv
import os


import pandas as pd
'''
os.chdir(r'D:/STUDY/data/bamboo/ALL0/arcpy/')#ALL\
work_path = os.getcwd()
file_path = os.path.join(work_path,'HL_2018.csv')


data = pd.read_csv(file_path,engine = 'python')'''
#初始化数据集
filename = os.listdir(r'D:/STUDY/data/bamboo/ALL0/1/')
data = pd.read_excel(r'D:/STUDY/data/bamboo/ALL0/arcpy/AR_2014.xlsx',header=None,dtype=object,index ='Timestamp')#read _csv,header=None)
#print(data)
#查看数据
#data.head()#

#X = data.iloc[:,arcpy:]
#y = data.iloc[:,arcpy]

#num_lines=correlation_slope_analysis

#out = X.rolling(num_lines).mean()
#print(out)





'''
df['DOY','WS_1m','WS_2m','WS_5m','WS_10m','WS_15m','WS_25m','WD','Ta_1m','Ta_2m','Ta_5m','Ta_10m',
         'Ta_15m','Ta_25m','RH_1m','RH_2m','RH_5m','RH_10m','RH_15m','RH_25m','Rain','P','IRT_1','IRT_2','AR','DR','UR',
         'DLR_cor','ULR_cor','Rn','Gs_1','Gs_2','Gs_3','TCAV','Ms_2cm','Ms_4cm_1','Ms_4cm_2','Ms_4cm_3','Ms_6cm',
         'Ms_10cm_1','Ms_10cm_2','Ms_10cm_3','Ms_15cm','Ms_20cm','Ms_30cm','Ms_40cm','Ms_60cm','Ms_80cm','Ms_120cm',
         'Ms_160cm','Ms_200cm','Ms_240cm','Ms_280cm','Ms_320cm','Ts_0cm','Ts_2cm','Ts_4cm_1','Ts_4cm_2','Ts_4cm_3',
         'Ts_6cm','Ts_10cm_1','Ts_10cm_2','Ts_10cm_3','Ts_15cm','Ts_20cm','Ts_30cm','Ts_40cm','Ts_60cm','Ts_80cm',
         'Ts_120cm','Ts_160cm','Ts_200cm','Ts_240cm','Ts_280cm','Ts_320cm']
for i,row in enumerate(X):
    if (i % num_lines) == 0 and i != 0:
        average = sum(data[i - num_lines:i]) / num_lines
        X.append(average)

    data.append((row[52560]))

'''
'''
X = data.iloc[arcpy:,arcpy:]
df = pd.DataFrame(X)
print(len(df))
Data_0 = []
i = 0
while i <= len(df):
    Data0 = df['Ta_5m','RH_5m','Ws_10m','WD','Rain_Tot','DR',
              'UR','DLR','ULR','Rn','Gs_1','Gs_2','Gs_3','Ms_2cm','Ms_4cm',
              'Ms_10cm','Ms_20cm','Ms_40cm','Ms_80cm','Ms_120cm','Ms_160cm',
              'Ts_0cm','Ts_2cm','Ts_4cm','Ts_10cm','Ts_20cm','Ts_40cm',
              'Ts_80cm','Ts_120cm','Ts_160cm','TCAV','Press'][i:i+correlation_slope_analysis] #每间隔3个数据取一次数
    Data1 = sum(Data0)/len(Data0)  #求取每组数据的平均值
    #Data1 = Data0.mean()
    Data_0.append(Data1)
    i = i+correlation_slope_analysis
    print(Data_0)
    Data_0.to_excel(r'D:/STUDY/data/bamboo/ALL0/result1/HL_2018.xlsx')
    print('********文件处理成功')
    '''

import numpy as np
df00 = pd.read_excel(r'D:/STUDY/data/bamboo/ALL0/arcpy/AR_2014.xlsx',header=None,index ='Timestamp')#, header=0)#不去掉表头
head = df00.iloc[0]


df = data.iloc[0:,1:]  # result2
row = df
numpermean = 3
(means) = [np.mean(row[i:(min(len(row), i + numpermean))]) \
             for i in range(0, len(row), numpermean)]

data1 = pd.DataFrame((means))
print(data1)
#df_test = pd.DataFrame(np.column_stack([(means)]),columns=head)
#print(df_test)
data1 = pd.DataFrame(data1)
#print(data1)
#data1 = pd.DataFrame(np.column_stack([(means)]))#.set_index('Ta_5m')

data1.to_excel(r'D:/STUDY/data/bamboo/ALL0/test.xlsx')
print('********文件处理成功')

'''
#columns=[head])#,columns=[head])#,index=arcpy)#,dtype=object,columns=[head])
#print(data1)
#data1 = data1.append(data1, ignore_index=True)
,columns=['DOY','WS_1m','WS_2m','WS_5m','WS_10m','WS_15m','WS_25m','WD','Ta_1m','Ta_2m','Ta_5m','Ta_10m',
         'Ta_15m','Ta_25m','RH_1m','RH_2m','RH_5m','RH_10m','RH_15m','RH_25m','Rain','P','IRT_1','IRT_2','AR','DR','UR',
         'DLR_cor','ULR_cor','Rn','Gs_1','Gs_2','Gs_3','TCAV','Ms_2cm','Ms_4cm_1','Ms_4cm_2','Ms_4cm_3','Ms_6cm',
         'Ms_10cm_1','Ms_10cm_2','Ms_10cm_3','Ms_15cm','Ms_20cm','Ms_30cm','Ms_40cm','Ms_60cm','Ms_80cm','Ms_120cm',
         'Ms_160cm','Ms_200cm','Ms_240cm','Ms_280cm','Ms_320cm','Ts_0cm','Ts_2cm','Ts_4cm_1','Ts_4cm_2','Ts_4cm_3',
         'Ts_6cm','Ts_10cm_1','Ts_10cm_2','Ts_10cm_3','Ts_15cm','Ts_20cm','Ts_30cm','Ts_40cm','Ts_60cm','Ts_80cm',
         'Ts_120cm','Ts_160cm','Ts_200cm','Ts_240cm','Ts_280cm','Ts_320cm'])
         columns=[X.iloc[0,arcpy:]]
         
#print(data1)
#data1.to_csv(r'D:/STUDY/data/bamboo/ALL0/result1/HL_2018.csv')'''
''','Ta_5m','RH_5m','Ws_10m','WD','Rain_Tot','DR',
              'UR','DLR','ULR','Rn','Gs_1','Gs_2','Gs_3','Ms_2cm','Ms_4cm',
              'Ms_10cm','Ms_20cm','Ms_40cm','Ms_80cm','Ms_120cm','Ms_160cm',
              'Ts_0cm','Ts_2cm','Ts_4cm','Ts_10cm','Ts_20cm','Ts_40cm',
              'Ts_80cm','Ts_120cm','Ts_160cm','TCAV','Press')'''