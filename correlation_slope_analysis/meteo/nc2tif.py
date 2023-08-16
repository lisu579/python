clc;
clear;

% % 批读取NC文件的准备工作
datadir = 'E:\CS_You\GLDAS\'; %指定批量数据所在的文件夹
filelist = dir([datadir, '*.nc4']); % 列出所有满足指定类型的文件

k = length(filelist);

for i = 1:k % 依次读取并处理
% % 批量读取NC文件
ncFilePath = ['E:\CS_You\GLDAS\',filelist(i).name]; %设定NC路径
              outFileName = filelist(i).name(1:33); % 输出文件名，(1:33)
即为第1 - 33
个字符

% % 读取变量值
lon = ncread(ncFilePath, 'lon'); % 读取经度信息（范围、精度）
lat = ncread(ncFilePath, 'lat'); % 读取维度信息
time = ncread(ncFilePath, 'time'); % 读取时间序列
pre = ncread(ncFilePath, 'Qle_tavg'); % 获取“潜热通量”变量数据

                                                % % 存为tif格式
b = flipud(pre
');
bb = rot90(b, 2);
data = fliplr(bb); % 镜像反转，否则栅格的南北朝向颠倒

R = georasterref('RasterSize', size(data), 'Latlim', [double(min(lat)) double(max(lat))], 'Lonlim',
                 [double(min(lon)) double(max(lon))]);
geotiffwrite(['E:\CS_You\GLDAS\TIFF\',outFileName,' - Qle_tavg.tif'], data, R);   % 输出路径
              disp([outFileName, 'done'])

              end
              disp('finish!')
