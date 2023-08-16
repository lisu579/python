import os
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import shapely
import rasterio
from rasterio.mask import mask

from mgwr.gwr import GWR, MGWR
#用的时候可以换成MGWR
from mgwr.sel_bw import Sel_BW

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn import preprocessing

import pandas as pd
import geopandas as gpd

import seaborn as sns
sns.set_style("white")
from datetime import datetime

# 训练数据读取处理
data_folder = r'D:\Data\paperData\GForkuor_Shapefiles'
inner_path = os.path.join(data_folder,'samples_inner.shp')
soc_path = os.path.join(data_folder, 'soc_inner.txt')
soc_df= pd.read_csv(soc_path, '\t')
inner_gdf = gpd.read_file(inner_path)

## 采样点与NDVI、BI、高程等信息合并
inner_soc_gdf = pd.merge(inner_gdf, soc_df, on="ID")

inner_soc_gdf['X'] = inner_soc_gdf['geometry'].x.values
inner_soc_gdf['Y'] = inner_soc_gdf['geometry'].y.values

y = inner_soc_gdf['SOC'].values.reshape((-1,1))
X = inner_soc_gdf[['June_NDVI','June_BI','Elevation']].values
u = inner_soc_gdf['X']
v = inner_soc_gdf['Y']
coords = list(zip(u,v))
## 数据集划分与标准化
cal_coords,pred_coords,cal_X,pred_X,cal_y,pred_y = train_test_split(coords, X, y, test_size=0.3, random_state=42)
scaler = preprocessing.StandardScaler().fit(cal_X)
cal_X_scaled = scaler.transform(cal_X)
pred_X_scaled = scaler.transform(pred_X)

# GWR模型构建
gwr_selector = Sel_BW(cal_coords, cal_y, cal_X_scaled)
gwr_bw = gwr_selector.search(bw_min=2)
print(gwr_bw)
model = GWR(cal_coords, cal_y, cal_X_scaled, gwr_bw)
gwr_results = model.fit()

scale = gwr_results.scale
residuals = gwr_results.resid_response

pred_coords_np = np.array(pred_coords)
pred_results = model.predict(pred_coords_np, pred_X_scaled, scale, residuals)
print(r2_score(pred_y.flatten(),pred_results.predictions.flatten()))

# 栅格数据读取处理
topo_folder = r'D:\Data\paperData\Forkuor_Topo_Climatic_Data'
landsat_folder = r'D:\Data\paperData\Forkuor_Landsat_Bands_Indices'

june_ndvi_path = os.path.join(landsat_folder, 'June_NDVI.tif')
june_bi_path = os.path.join(landsat_folder, 'June_BI.tif')
elevation_path = os.path.join(topo_folder, 'Elevation.tif')

## 获取训练样本点的区域范围
bound = shapely.geometry.box(*inner_gdf.total_bounds)

with rasterio.open(june_ndvi_path) as src:
    ## 裁剪栅格数据
    june_ndvi, out_transform = mask(src, [bound], crop=True)
    out_meta = src.meta
with rasterio.open(june_bi_path) as src:
    june_bi, _ = mask(src, [bound], crop=True)
with rasterio.open(elevation_path) as src:
    elevation, _ = mask(src, [bound], crop=True)
## 结果tif输出参数
out_meta.update({"driver": "GTiff",
                 "height": june_ndvi.shape[1],
                 "width": june_ndvi.shape[2],
                 "transform": out_transform})
## 栅格像素坐标XY计算
height = june_ndvi.shape[1]
width = june_ndvi.shape[2]
cols, rows = np.meshgrid(np.arange(width), np.arange(height))
xs, ys = rasterio.transform.xy(out_transform, rows, cols)
lons= np.array(xs)
lats = np.array(ys)

## GWR用于裁剪区域预测
i=0
map_preds = []
for col, row in zip(cols.reshape(-1,), rows.reshape(-1,)):
    pix_coords = np.array([lons[row][col], lats[row][col]]).reshape(1,-1)
    pix_X = np.array([june_ndvi[0][row][col],june_bi[0][row][col],elevation[0][row][col]]).reshape(1,-1)
    pix_X_scaled = scaler.transform(pix_X)
    pred_results = model.predict(pix_coords, pix_X_scaled, scale, residuals)
    map_preds.append(pred_results.predictions[0][0])
    i = i+1
    if i%50000==0:
        print('-------{}, {}, {}, {}---------'.format(datetime.now().strftime("%H:%M:%S"), i, col, row))
map_preds_2d = np.array(map_preds).reshape(3429, -1)
map_preds_2d[map_preds_2d>5] = 5
map_preds_2d[map_preds_2d<0] = 0
map_preds_2d = np.expand_dims(map_preds_2d, axis=0)
# from rasterio.plot import show, show_hist
# show(map_preds_2d, cmap='viridis')

## 结果tif文件保存写入
with rasterio.open("D:/SOC_preds.tif", "w", **out_meta) as dst:
    dst.write(map_preds_2d)