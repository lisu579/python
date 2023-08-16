// 定义范围
var
geometry = ee.FeatureCollection("users/lisuxun579/Bamboo_shp");
Map.centerObject(geometry, 8)

var
colorizedVis = {
    min: -0.8,
    max: 0.8,
    palette: ['blue', 'white', 'green'],
};
// 去云
// cloud
mask
function
maskL8sr(image)
{
// Bits
3 and 5
are
cloud
shadow and cloud, respectively.
    var
cloudShadowBitMask = (1 << 3);
var
cloudsBitMask = (1 << 5);
// Get
the
pixel
QA
band.
    var
qa = image.select('pixel_qa');
// Both
flags
should
be
set
to
zero, indicating
clear
conditions.
    var
mask = qa.bitwiseAnd(cloudShadowBitMask).eq(0)
           . and (qa.bitwiseAnd(cloudsBitMask).eq(0));
return image.updateMask(mask);
}
// SR
var
col = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
    .map(maskL8sr)
    .filterDate('2020-01-01', '2021-12-31')
    .filterBounds(geometry)
    .map(function(image)
{
    var
ndvi = image.normalizedDifference(['B5', 'B4']).rename('NDVI');
return image.addBands(ndvi)
})
.select('NDVI');

Map.addLayer(col.mean().clip(geometry), colorizedVis, 'col');

print(ui.Chart.image.series(col, geometry, ee.Reducer.mean(), 500));
// 计算月平均
var
years = ee.List.sequence(2020, 2021);
var
months = ee.List.sequence(1, 12);
var
landsat8monthlymeanNDVI = ee.ImageCollection.fromImages(
    years.map(function(y)
{
return months.map(function(m)
{
return col.filter(ee.Filter.calendarRange(y, y, 'year')).filter(ee.Filter.calendarRange(m, m, 'month')).mean().set(
    'year', y).set('month', m).set('system:time_start', ee.Date.fromYMD(y, m, 1));
});
}).flatten()
);
print(ui.Chart.image.series(landsat8monthlymeanNDVI, geometry, ee.Reducer.mean(), 500));

// 提取像元值
var
ft = ee.FeatureCollection(ee.List([]))

var
fill = function(img, ini)
{

    var
inift = ee.FeatureCollection(ini)
        // table is shapefile
var
pts = ee.FeatureCollection(table)

var
ft2 = img.sampleRegions({
    collection: pts,
    properties: ee.List(['class']),
    scale: 30
});
var
date = img.date().format()
var
ft3 = ft2.map(function(f)
{
return f.set("date", date)})
return inift.merge(ft3)
}

// Iterates
over
the
ImageCollection
var
newft = ee.FeatureCollection(col.iterate(fill, ft))

Export.table.toDrive({
    collection: newft,
    description: 'sample_get',
    fileFormat: 'CSV'
});




