import pandas as pd
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize
from scipy.stats import gaussian_kde
from matplotlib import rcParams
config={"font.family":'Times New Roman',"font.size":16,"mathtext.fontset":'stix'}
rcParams.update(config)
# 读取数据
filename=r'D:\STUDY\data\test\t.xlsx'
df2=pd.read_excel(filename)#读取文件
x=df2['data1'].values.ravel()
y=df2['data2'].values.ravel()
N = len(df2['data1'])
#绘制拟合线
x2 = np.linspace(-10,30)
y2 = x2
def f_1(x,A,B):
    return A*x + B
A1,B1 = optimize.curve_fit(f_1,x,y)[0]
y3 = A1*x + B1
# Calculate the point density
xy = np.vstack([x,y])
z = gaussian_kde(xy)(xy)
norm = Normalize(vmin = np.min(z), vmax = np.max(z))


#开始绘图
fig,ax=plt.subplots(figsize=(8,5),dpi=600)
scatter=ax.scatter(x,y,marker='o',c=z*100,edgecolors='',s=15,label='LST',cmap='Spectral_r')
cbar=plt.colorbar(scatter,shrink=1,orientation='vertical',extend='both',pad=0.015,aspect=30,label='frequency')
cbar.ax.locator_params(nbins=8)
cbar.ax.set_yticklabels([0.005,0.010,0.015,0.020,0.025,0.030,0.035])#0,0.005,0.010,0.015,0.020,0.025,0.030,0.035
ax.plot(x2,y2,color='k',linewidth=1.5,linestyle='--')
ax.plot(x,y3,color='r',linewidth=2,linestyle='-')
fontdict1 = {"size":16,"color":"k",'family':'Times New Roman'}
ax.set_xlabel("ET",fontdict=fontdict1)
ax.set_ylabel("TEM",fontdict=fontdict1)
# ax.grid(True)
ax.set_xlim((1683,1793))
ax.set_ylim((473,1088))
ax.set_xticks(np.arange(0,1831,step=20))
ax.set_yticks(np.arange(500,1100,step=100))
plt.savefig(r'D:\STUDY\data\test\cor_tem.png',dpi=800,bbox_inches='tight',pad_inches=0)
plt.show()