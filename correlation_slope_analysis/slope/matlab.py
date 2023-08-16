%将两者多年的数据放在三个不同的矩阵中
nppsum=zeros(653*922,21);
for year=2000:2020
    filename=strcat('D:\STUDY\data\test\et\',int2str(year),'.tif');
    data=importdata(filename);
    data=reshape(data,653*922,1);
    nppsum(:,year-1999)=data;
end

temsum=zeros(653*922,21);
for year=2000:2020
    filename=strcat('D:\STUDY\data\test\tem\',int2str(year),'.tif');
    data=importdata(filename);
    data=reshape(data,653*922,1);
    wcsum(:,year-1999)=data;
end
%相关性和显著性
npp_wc_xgx=zeros(653,922);
npp_wc_p=zeros(653,922);
for i=1:length(nppsum)
    npp=nppsum(i,:);
    if min(npp)>0 %注意这里的NPP的有效范围是大于0，如果自己的数据有效范围有小于0的话，则可以不用加这个
        wc=wcsum(i,:);
         [r2,p2]=corrcoef(npp,wc);
         npp_wc_xgx(i)=r2(2);
         npp_wc_p(i)=p2(2);
    end
end
filename5='F:\result\et_tem相关性.tif';
filename6='F:\et_tem显著性.tif';

[a,R]=geotiffread('F:\data\water_yield.tif');%先导入投影信息
info=geotiffinfo('F:\data\water_yield.tif');
%%输出图像
geotiffwrite(filename5,npp_wc_xgx,R,'GeoKeyDirectoryTag',info.GeoTIFFTags.GeoKeyDirectoryTag);
geotiffwrite(filename6,npp_wc_p,R,'GeoKeyDirectoryTag',info.GeoTIFFTags.GeoKeyDirectoryTag);