#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Details:  散点图绘制
"""
import time
import numpy as np
import pandas as pd
import matplotlib.colors as colors
import matplotlib.pyplot as plt


def density_calc(x, y, radius):
    """
    散点密度计算（以便给散点图中的散点密度进行颜色渲染）
    :param x:
    :param y:
    :param radius:
    :return:  数据密度
    """
    res = np.empty(len(x), dtype=np.float32)
    for i in range(len(x)):
        print(i)
        res[i] = np.sum((x > (x[i] - radius)) & (x < (x[i] + radius))
                        & (y > (y[i] - radius)) & (y < (y[i] + radius)))
    return res


# Script Start...
start = time.process_time()

url_i = r"D:\STUDY\data\VOD\correlation\bamboo_H_VOD.xls"

savefig_name = r"D:\STUDY\data\VOD\correlation\cor.png"

# ------------ read data  -----------------
matrix_i = pd.read_excel(url_i).values
sevp_i = matrix_i[:, 0]   # 观测数据
estimate_i = matrix_i[:, 1]  # 预测数据

# ----------- Define Parameters ------------
radius = 6 # 半径
colormap = plt.get_cmap("jet")  # 色带
marker_size = 0.5  # 散点大小
xrange = [0, 1]
yrange = [0, 50]
xticks = np.linspace(0, 1, 1)
yticks = np.linspace(0, 50, 1)
xlabel = "VOD"
ylabel_i = "Height"

cbar_ticks = [10**0, 10**1, 10**2, 10**3, 10**4, 10**5]
font = {'family': 'Times New Roman',
        'weight': 'bold',
        'size': 6}

# -----------------  Plot Start  -----------------
fig = plt.figure(1, facecolor="grey")

# ---------------  sub plot no.arcpy  ----------------
plt.subplot(1, 1, 1, aspect="equal")
Z1 = density_calc(sevp_i, estimate_i, radius)
plt.scatter(sevp_i, estimate_i, c=Z1, cmap=colormap, marker=".", s=marker_size,
            norm=colors.LogNorm(vmin=Z1.min(), vmax=0.5 * Z1.max()))
plt.xlim(xrange)
plt.ylim(yrange)
#plt.xticks(xticks, fontproperties='Times New Roman', size=6)
#plt.yticks(yticks, fontproperties='Times New Roman', size=6)
plt.xlabel(xlabel, fontdict=font)
plt.ylabel(ylabel_i, fontdict=font)
plt.grid(linestyle='--', color="grey")
plt.plot(xrange, yrange, color="k", linewidth=0.8, linestyle='--')
plt.rc('font', **font)
# color bar
cbar = plt.colorbar(orientation='horizontal', extend="both", pad=0.1)  # 显示色带
cbar.set_label("Scatter Density", fontdict=font)
cbar.set_ticks(cbar_ticks)
cbar.ax.tick_params(which="major", direction="in", length=2, labelsize=6)  # 主刻度
cbar.ax.tick_params(which="minor", direction="in", length=0)  # 副刻度


# save figure
fig.tight_layout()
plt.savefig(savefig_name, dpi=600)
plt.show()

elapsed = time.process_time() - start
print("This program totally costs {0} seconds!".format(elapsed))
print(" .... All is OK!!")
