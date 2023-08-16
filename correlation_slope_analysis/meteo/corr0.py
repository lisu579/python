import matplotlib.pyplot as plt
import numpy as np
import scipy
import gdal
from scipy.stats import gaussian_kde

def calculate_statis(x, y):
# 相关数据统计

res = scipy.stats.linregress(x, y)
sample_corr = res.rvalue
sample_slope = res.slope
sample_inter = res.intercept
sample_size = x.shape[0]
bias = x - y
mean_bias = np.mean(bias)
max_bias = np.max(bias)
min_bias = np.min(bias)
abs_mean_bias = np.mean(np.abs(bias))
std_bias = np.sqrt(np.power(bias, 2).sum() / (sample_size - 1))
rmse_bias = np.sqrt(np.power(bias, 2).sum() / (sample_size))

print("样本数量：%d" % sample_size)
print("样本斜率：%.4f,截距：%.4f,相关性：%.4f" % (sample_slope, sample_inter, sample_corr))
print("平均偏差：%.3f,最大偏差：%.3f,最小偏差:%.3f,平均绝对偏差:%.3f" % (mean_bias, max_bias, min_bias, abs_mean_bias))
print("偏差标准差：%.3f,偏差RMSE:%.3f" % (std_bias, rmse_bias))
return sample_corr, mean_bias, std_bias, sample_size

def draw_pts_scatter(x_data, y_data, range_min, range_max, title