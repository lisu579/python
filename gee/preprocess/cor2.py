
from statistics import mean
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import explained_variance_score,r2_score,median_absolute_error,mean_squared_error,mean_absolute_error
from scipy import stats
import numpy as np
from matplotlib import rcParams

config = {"font.family":'Times New Roman',"font.size": 16,"mathtext.fontset":'stix'}
rcParams.update(config)

# 读取数据
filename=r'D:\STUDY\data\VOD\correlation\bamboo_H_VOD.xls'
df2=pd.read_excel(filename)#读取文件
x=df2['VOD'].values.ravel()
y=df2['Height'].values.ravel()
N = len(df2['VOD'])
def scatter_out_1(x,y): ## x,y为两个需要做对比分析的两个量。
    # ==========计算评价指标==========
    BIAS = mean(x - y)
    MSE = mean_squared_error(x, y)
    RMSE = np.power(MSE, 0.5)
    R2 = r2_score(x, y)
    MAE = mean_absolute_error(x, y)
    EV = explained_variance_score(x, y)
    print('==========算法评价指标==========')
    print('BIAS:', '%.3f' % (BIAS))
    print('Explained Variance(EV):', '%.3f' % (EV))
    print('Mean Absolute Error(MAE):', '%.3f' % (MAE))
    print('Mean squared error(MSE):', '%.3f' % (MSE))
    print('Root Mean Squard Error(RMSE):', '%.3f' % (RMSE))
    print('R_squared:', '%.3f' % (R2))
    # ===========Calculate the point density==========
    xy = np.vstack([x, y])
    z = stats.gaussian_kde(xy)(xy)
    # ===========Sort the points by density, so that the densest points are plotted last===========
    idx = z.argsort()
    x, y, z = x[idx], y[idx], z[idx]
    def best_fit_slope_and_intercept(xs, ys):
        m = (((mean(xs) * mean(ys)) - mean(xs * ys)) / ((mean(xs) * mean(xs)) - mean(xs * xs)))
        b = mean(ys) - m * mean(xs)
        return m, b
    m, b = best_fit_slope_and_intercept(x, y)
    regression_line = []
    for a in x:
        regression_line.append((m * a) + b)
    fig,ax=plt.subplots(figsize=(12,9),dpi=600)
    scatter=ax.scatter(x,y,marker='o',c=z*100,edgecolors='',s=15,label='LST',cmap='Spectral_r')
    cbar=plt.colorbar(scatter,shrink=1,orientation='vertical',extend='both',pad=0.015,aspect=30,label='frequency')
    plt.plot([0,25],[0,25],'black',lw=1.5)  # 画的1:1线，线的颜色为black，线宽为0.8
    plt.plot(x,regression_line,'red',lw=1.5)      # 预测与实测数据之间的回归线
    plt.axis([0,25,0,25])  # 设置线的范围
    plt.xlabel('OBS',family = 'Times New Roman')
    plt.ylabel('PRE',family = 'Times New Roman')
    plt.xticks(fontproperties='Times New Roman')
    plt.yticks(fontproperties='Times New Roman')
    plt.text(1,24, '$N=%.f$' % len(y), family = 'Times New Roman') # text的位置需要根据x,y的大小范围进行调整。
    plt.text(1,23, '$R^modis_preprocess=%.3f$' % R2, family = 'Times New Roman')
    plt.text(1,22, '$BIAS=%.4f$' % BIAS, family = 'Times New Roman')
    plt.text(1,21, '$RMSE=%.3f$' % RMSE, family = 'Times New Roman')
    plt.xlim(0,25)                                  # 设置x坐标轴的显示范围
    plt.ylim(0,25)                                  # 设置y坐标轴的显示范围
    plt.savefig(r'D:\STUDY\data\VOD\correlation\corr2.png',dpi=800,bbox_inches='tight',pad_inches=0)
    plt.show()