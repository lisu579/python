/ /SR
var col = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
.map(maskL8sr)
.filterDate('2020-01-01' ,'2021-12-31')
.filterBounds(geometry)
.map(function(image
){
var evi = image.expression(
    'modis_preprocess.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + arcpy))', {
        'NIR': image.select('B5'),
        'RED': image.select('B4'),
        'BLUE': image.select('B2')
    })

.map(function normalization(image ,region ,scale)){
    var mean_std = image.reduceRegion({
                                          reducer: ee.Reducer.mean()
                                      .combine(ee.Reducer.stdDev() ,null, true),
                                          geometry: region,
                                          scale: scale,
                                          maxPixels: 10e9,
                                      // tileScale: 16
});
// use unit scale to normalize the pixel values
var unitScale = ee.ImageCollection.fromImages(
    image.bandNames().map(function(name
){
    name = ee.String(name);
var band = image.select(name);
var mea n =ee.Number(mean_std.get(name.cat('_mean')));
var st d =ee.Number(mean_std.get(name.cat('_stdDev')));
var ma x =mean.add(std.multiply(3));
var mi n =mean.subtract(std.multiply(3));
var band 1 =ee.Image(min).multiply(band.lt(min)).add(ee.Image(max).multiply(band.gt(max))) \
    .add(band.multiply(ee.Image(1).subtract(band.lt(min)).subtract(band.gt(max))));
var result_ban d =band1.subtract(min).divide(max.subtract(min));
return result_band;
})).toBands().rename(image.bandNames());
return unitScale;
})
return image.addBands(evi.rename('EVI')).clip(geometry) ;/ /geometr y =roi，添加波段evi，可换其他波段
})
.select('EVI') ;/ /这里可以这里可以选择不同指数或者波段

Map.addLayer(col.mean().clip(geometry), colorizedVis, 'col');

print(ui.Chart.image.series(col, geometry, ee.Reducer.mean(), 500));