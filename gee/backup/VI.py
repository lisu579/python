
 //定义范围
var geometry = ee.FeatureCollection("users/lisuxun579/Bamboo_shp");
Map.centerObject(geometry,8)
 //0.1>>1
var colorizedVis = {
  min: -1,
  max: 1,
  palette: ['blue', 'white', 'green'],
};
//去云
//cloud mask
function maskL8sr(image) {
  // Bits 3 and 5 are cloud shadow and cloud, respectively.
  var cloudShadowBitMask = (1 << 3);
  var cloudsBitMask = (1 << 5);
  // Get the pixel QA band.
  var qa = image.select('pixel_qa');
  // Both flags should be set to zero, indicating clear conditions.
  var mask = qa.bitwiseAnd(cloudShadowBitMask).eq(0)
                 .and(qa.bitwiseAnd(cloudsBitMask).eq(0));
  return image.updateMask(mask);
}
//SR
var col = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
.map(maskL8sr)
.filterDate('2020-01-01','2021-12-31')
.filterBounds(geometry)
.map(function(image){
   var evi = image.expression(
    'modis_preprocess.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + arcpy))', {
      'NIR': image.select('B5'),
      'RED': image.select('B4'),
      'BLUE': image.select('B2')
});
return image.addBands(evi.rename('EVI')).clip(geometry);//geometry=roi，添加波段evi，可换其他波段


})
.select('EVI');//这里可以这里可以选择不同指数或者波段

//;
Map.addLayer(col.mean().clip(geometry), colorizedVis, 'col');

print(ui.Chart.image.series(col, geometry, ee.Reducer.mean(), 500));

var scol_clip =image.first().clip(geometry);


//归一化
function normalization(image,region,scale){
var mean_std = image.reduceRegion({
  reducer: ee.Reducer.mean()
            .combine(ee.Reducer.stdDev(),null, true),
  geometry: region,
  scale: scale,
  maxPixels: 10e9,
  // tileScale: 16
});
// use unit scale to normalize the pixel values
var unitScale = ee.ImageCollection.fromImages(
  image.bandNames().map(function(name){
    name = ee.String(name);
    var band = image.select(name);
    var mean=ee.Number(mean_std.get(name.cat('_mean')));
    var std=ee.Number(mean_std.get(name.cat('_stdDev')));
    var max=mean.add(std.multiply(3));
    var min=mean.subtract(std.multiply(3));
    var band1=ee.Image(min).multiply(band.lt(min)).add(ee.Image(max).multiply(band.gt(max)))
                        .add(band.multiply(ee.Image(1).subtract(band.lt(min)).subtract(band.gt(max))));
    var result_band=band1.subtract(min).divide(max.subtract(min));
    return result_band;
})).toBands().rename(image.bandNames());
  return unitScale;
}
//归一化前的结果
var before_chart=ui.Chart.image.histogram(scol_clip.select(["B4","EVI"]), geometry, 500);
print(before_chart);
//让影像进行归一化函数处理后的结果
var normal_image=normalization(scol_clip,hh,1000)
print(normal_image)
//归一化后的结果
var after_chart=ui.Chart.image.histogram(normal_image.select(["B4","EVI"]), geometry, 500)
print(after_chart)



//计算月平均
var years = ee.List.sequence(2020, 2021);
var months = ee.List.sequence(1, 12);
var landsat8monthlymeanEVI = ee.ImageCollection.fromImages(
  years.map(function (y) {
    return months.map(function(m) {
    return col.filter(ee.Filter.calendarRange(y,y, 'year')).filter(ee.Filter.calendarRange(m, m, 'month')).mean().set('year', y).set('month', m).set('system:time_start', ee.Date.fromYMD(y, m, 1));
    });
  }).flatten()
);
print(ui.Chart.image.series(landsat8monthlymeanEVI, geometry, ee.Reducer.mean(), 500));


// 提取像元值
var ft = ee.FeatureCollection(ee.List([]))

var fill = function(img, ini) {

  var inift = ee.FeatureCollection(ini)
//table is shapefile
  var pts = ee.FeatureCollection(table)

  var ft2 = img.sampleRegions({
  collection:pts,
  properties:ee.List(['class']),
  scale:30
  });
  var date = img.date().format()
  var ft3 = ft2.map(function(f){return f.set("date", date)})
  return inift.merge(ft3)
}

// Iterates over the ImageCollection
var newft = ee.FeatureCollection(col.iterate(fill, ft))

Export.table.toDrive({
  collection: newft,
  description: 'evi',
  fileFormat: 'CSV'
});

