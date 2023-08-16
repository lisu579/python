# -*- coding: utf-8 -*-
import cartopy.mpl.ticker as cticker
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from cartopy.mpl.ticker import LongitudeFormatter ,LatitudeFormatter
import cartopy.crs as ccrs
import cartopy.feature as cfeature
p=r'D:\STUDY\data\meteology\meteo.nc'
data=xr.open_dataset(p).sel(time=slice("2020","2020"))
u=data.u100
v=data.v100
w=np.sqrt(u*u+v*v)
lon=data.longitude.data
lat=data.latitude.data
def make_map(ax,title,box,xstep,ystep):
    # set_extent  set crs
    ax.set_extent(box, crs=ccrs.PlateCarree())
    ax.coastlines(scale)  # set coastline resolution
    # set coordinate axis
    ax.set_xticks(np.arange(box[0], box[1], xstep),crs=ccrs.PlateCarree())
    ax.set_yticks(np.arange(box[2], box[3], ystep),crs=ccrs.PlateCarree())
    ax.xaxis.set_major_formatter(cticker.LongitudeFormatter())
    #经度0不加标识
    ax.yaxis.set_major_formatter(cticker.LatitudeFormatter())
    ax.set_title(title, fontsize=10, loc='center')
    return ax
fig=plt.figure(figsize=(80,50))
x,y=np.meshgrid(lon,lat)
box1 = [90, 150, 0, 55]
scale = '110m'
xstep, ystep = 30, 40
cmap=plt.get_cmap('Oranges')#'Blues''RdYlBu_r'
titl=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec']

for i in range(12):
    print(i)
    proj=ccrs.PlateCarree(central_longitude=120)
    ax=fig.add_subplot(3,4,i+1,projection=proj)
    make_map(ax,str(titl[i]),box1,40,20)
    cb=ax.quiver(x[::12,::12],y[::12,::12],u.data[i,:,:][::12,::12],v.data[i,:,:][::12,::12],pivot='mid',\
    width=0.0036,scale=150,transform=ccrs.PlateCarree(),color='k',angles='xy',zorder=1)
    cp=ax.contourf(lon,lat,w.data[i],zorder=0,transform=ccrs.PlateCarree(),cmap=cmap,levels=np.arange(0,21,2),extend='both')
plt.show()
