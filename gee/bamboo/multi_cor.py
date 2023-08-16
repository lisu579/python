import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import Series,DataFrame
from sklearn import datasets
import seaborn as sns

#导入鸢尾花iris数据集（方法一）
#该方法更有助于理解数据集

filename=r'D:\STUDY\data\VOD\correlation\bamboo_H_VOD.xls'
df2=pd.read_excel(filename)#读取文件
x=df2['VOD_AGB1'].values.ravel()
y=df2['VOD_AGB2'].values.ravel()

y_1 = np.array(['bamboo'])
pd_iris = pd.DataFrame(np.hstack((x, y_1.reshape(150,1))),columns=['VOD_AGB1','VOD_AGB2','VOD_AGB3','class'])
pd_iris.describe()
#astype修改pd_iris中数据类型object为float64
pd_iris['VOD_AGB1']=pd_iris['VOD_AGB1'].astype('float64')
pd_iris['VOD_AGB2']=pd_iris['VOD_AGB2'].astype('float64')
pd_iris['VOD_AGB3']=pd_iris['VOD_AGB3'].astype('float64')



#导入鸢尾花iris数据集（方法二）
#import seaborn as sns
#iris_sns = sns.load_dataset("iris")
g = sns.pairplot(pd_iris)
g.fig.set_size_inches(12,12)#figure大小
sns.set(style='whitegrid',font_scale=1.5)#文本大小
plt.savefig(r'D:\STUDY\data\VOD\correlation\corr2.png',dpi=800,bbox_inches='tight',pad_inches=0)
plt.show()