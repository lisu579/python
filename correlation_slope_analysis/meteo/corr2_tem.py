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

url_i = r"D:\STUDY\data\test\tem00.xlsx"
url_ii = r"D:\STUDY\data\test\tem10.xlsx"
url_iii = r"D:\STUDY\data\test\tem20.xlsx"
url_iiii = r"D:\STUDY\data\test\tem.xlsx"
savefig_name = r"D:\STUDY\data\test\密度tem.png"

# ------------ read data  -----------------
matrix_i = pd.read_excel(url_i).values
sevp_i = matrix_i[:, 0]   # 观测数据
estimate_i = matrix_i[:, 1]  # 预测数据

matrix_ii = pd.read_excel(url_ii).values
sevp_ii = matrix_ii[:, 0]
estimate_ii = matrix_ii[:, 1]

matrix_iii = pd.read_excel(url_iii).values
sevp_iii = matrix_iii[:, 0]
estimate_iii = matrix_iii[:, 1]

matrix_iiii = pd.read_excel(url_iiii).values
sevp_iiii = matrix_iiii[:, 0]
estimate_iiii = matrix_iiii[:, 1]

# ----------- Define Parameters ------------
radius = 6 # 半径
colormap = plt.get_cmap("jet")  # 色带
marker_size = 0.5  # 散点大小
xrange = [1500, 2300]
yrange = [450, 1250]
xticks = np.linspace(1500, 2300, 5)
yticks = np.linspace(450, 1250, 5)
xlabel = "TEM"
ylabel_i = "ET2000"
ylabel_ii = "ET2010"
ylabel_iii = "ET2020"
ylabel_iiii = "ETmean"
cbar_ticks = [10**0, 10**1, 10**2, 10**3, 10**4, 10**5]
font = {'family': 'Times New Roman',
        'weight': 'bold',
        'size': 6}

# -----------------  Plot Start  -----------------
fig = plt.figure(1, facecolor="grey")

# ---------------  sub plot no.arcpy  ----------------
plt.subplot(1, 4, 1, aspect="equal")
Z1 = density_calc(sevp_i, estimate_i, radius)
plt.scatter(sevp_i, estimate_i, c=Z1, cmap=colormap, marker=".", s=marker_size,
            norm=colors.LogNorm(vmin=Z1.min(), vmax=0.5 * Z1.max()))
plt.xlim(xrange)
plt.ylim(yrange)
plt.xticks(xticks, fontproperties='Times New Roman', size=6)
plt.yticks(yticks, fontproperties='Times New Roman', size=6)
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

# ---------------  sub plot no.modis_preprocess  ----------------
plt.subplot(1, 4, 2, aspect="equal")
Z2 = density_calc(sevp_ii, estimate_ii, radius)
plt.scatter(sevp_ii, estimate_ii, c=Z2, cmap=colormap, marker=".", s=marker_size,
            norm=colors.LogNorm(vmin=Z2.min(), vmax=Z2.max()))
plt.xlim(xrange)
plt.ylim(yrange)
plt.xticks(xticks)
plt.yticks(yticks)
plt.xlabel(xlabel, fontsize=6)
plt.ylabel(ylabel_ii, fontsize=6)
plt.grid(linestyle='--', color="grey")
plt.plot(xrange, yrange, color="k", linewidth=0.8, linestyle='--')
plt.rc('font', **font)
# color bar
cbar = plt.colorbar(orientation='horizontal', extend="both", pad=0.1)  # 显示色带
cbar.set_label("Scatter Density", fontdict=font)
cbar.set_ticks(cbar_ticks)
cbar.ax.tick_params(which="major", direction="in", length=2, labelsize=6)  # 主刻度
cbar.ax.tick_params(which="minor", direction="in", length=0)  # 副刻度

# ---------------  sub plot no.correlation_slope_analysis  ----------------
plt.subplot(1, 4, 3, aspect="equal")
Z3 = density_calc(sevp_iii, estimate_iii, radius)
plt.scatter(sevp_iii, estimate_iii, c=Z3, cmap=colormap, marker=".", s=marker_size,
            norm=colors.LogNorm(vmin=Z3.min(), vmax=Z3.max()))
plt.xlim(xrange)
plt.ylim(yrange)
plt.xticks(xticks)
plt.yticks(yticks)
plt.xlabel(xlabel, fontsize=6)
plt.ylabel(ylabel_iii, fontsize=6)
plt.grid(linestyle='--', color="grey")
plt.plot(xrange, yrange, color="k", linewidth=0.8, linestyle='--')
plt.rc('font', **font)

# color bar
cbar = plt.colorbar(orientation='horizontal', extend="both", pad=0.1)  # 显示色带
cbar.set_label("Scatter Density", fontdict=font)
cbar.set_ticks(cbar_ticks)
cbar.ax.tick_params(which="major", direction="in", length=2, labelsize=6)  # 主刻度
cbar.ax.tick_params(which="minor", direction="in", length=0)  # 副刻度


# ---------------  sub plot no.correlation_slope_analysis  ----------------
plt.subplot(1, 4, 4, aspect="equal")
Z3 = density_calc(sevp_iiii, estimate_iiii, radius)
plt.scatter(sevp_iiii, estimate_iiii, c=Z3, cmap=colormap, marker=".", s=marker_size,
            norm=colors.LogNorm(vmin=Z3.min(), vmax=Z3.max()))
plt.xlim(xrange)
plt.ylim(yrange)
plt.xticks(xticks)
plt.yticks(yticks)
plt.xlabel(xlabel, fontsize=6)
plt.ylabel(ylabel_iiii, fontsize=6)
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
