import numpy as np
import pandas as pd

#read excel file
excel_path = r'D:\STUDY\data\GEE\sample_get1.xls'
data = pd.read_excel(excel_path)

data['date'] = data.date
data['NDVI'] = data.NDVI #提取需要进行计算的一列

# Convert the date to datetime64
data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')

for i in data['NDVI'].groupby(data['date']).mean():
    print(i)
