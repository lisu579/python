#>>>>>>lc8反射率提取成功>>>>>


//Landsat8 SR数据去云

function rmCloud(image) {

var cloudShadowBitMask = (1 << 3);

var cloudsBitMask = (1 << 5);

var qa = image.select("pixel_qa");

var mask = qa.bitwiseAnd(cloudShadowBitMask).eq(0)

.and(qa.bitwiseAnd(cloudsBitMask).eq(0));

return image.updateMask(mask);

}



//从GEE 数据集导入Landsat 8数据

var L8_roi1 =ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')

.filterBounds(table2)

.filterDate('2020-03-01', '2020-03-31')

.median();

// 提取像元值

var pts = ee.FeatureCollection(table)

var ft2 = L8_roi1.sampleRegions({

collection:pts,

properties:ee.List(['class']),

scale:30

});



Export.table.toDrive({

collection: ft2,

folder:'bamboo',

description: 'bandreflectance_extract',

fileFormat: 'CSV'

});

