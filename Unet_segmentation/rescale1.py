int
ResampleGDAL(const
char * pszSrcFile, const char * pszOutFile, float
fResX = 1.0, float
fResY = 1.0, GDALResampleAlg
eResample = GRA_Bilinear)
{
    GDALAllRegister();
CPLSetConfigOption("GDAL_FILENAME_IS_UTF8", "NO");
GDALDataset * pDSrc = (GDALDataset *)
GDALOpen(pszSrcFile, GA_ReadOnly);
if (pDSrc == NULL)
{
return -1;
}


GDALDriver * pDriver = GetGDALDriverManager()->GetDriverByName("GTiff");
if (pDriver == NULL)
{
GDALClose((GDALDatasetH)
pDSrc);
return -2;
}
int
width = pDSrc->GetRasterXSize();
int
height = pDSrc->GetRasterYSize();
int
nBandCount = pDSrc->GetRasterCount();
GDALDataType
dataType = pDSrc->GetRasterBand(1)->GetRasterDataType();

char * pszSrcWKT = NULL;
pszSrcWKT = const_cast < char * > (pDSrc->GetProjectionRef());


double
dGeoTrans[6] = {0};
int
nNewWidth = width, nNewHeight = height;
pDSrc->GetGeoTransform(dGeoTrans);

bool
bNoGeoRef = false;
double
dOldGeoTrans0 = dGeoTrans[0];
// 如果没有投影，人为设置一个
if (strlen(pszSrcWKT) <= 0)
{
// OGRSpatialReference
oSRS;
// oSRS.SetUTM(50, true); // 北半球
东经120度
// oSRS.SetWellKnownGeogCS("WGS84");
// oSRS.exportToWkt( & pszSrcWKT);
// pDSrc->SetProjection(pszSrcWKT);

//
dGeoTrans[0] = 1.0;
pDSrc->SetGeoTransform(dGeoTrans);
//

bNoGeoRef = true;
}

// adfGeoTransform[0] / * top
left
x * /
// adfGeoTransform[1] / * w - e
pixel
resolution * /
// adfGeoTransform[2] / * rotation, 0 if image is "north up" * /
                                         // adfGeoTransform[3] / * top
left
y * /
// adfGeoTransform[4] / * rotation, 0 if image is "north up" * /
                                         // adfGeoTransform[5] / * n - s
pixel
resolution * /

dGeoTrans[1] = dGeoTrans[1] / fResX;
dGeoTrans[5] = dGeoTrans[5] / fResY;
nNewWidth = static_cast < int > (nNewWidth * fResX + 0.5);
nNewHeight = static_cast < int > (nNewHeight * fResY + 0.5);

// 创建结果数据集
GDALDataset * pDDst = pDriver->Create(pszOutFile, nNewWidth, nNewHeight, nBandCount, dataType, NULL);
if (pDDst == NULL)
{
GDALClose((GDALDatasetH)
pDSrc);
return -2;
}

pDDst->SetProjection(pszSrcWKT);
pDDst->SetGeoTransform(dGeoTrans);

void * hTransformArg = NULL;
hTransformArg = GDALCreateGenImgProjTransformer2((GDALDatasetH)
pDSrc, (GDALDatasetH)
pDDst, NULL); // GDALCreateGenImgProjTransformer((GDALDatasetH)
pDSrc, pszSrcWKT, (GDALDatasetH)
pDDst, pszSrcWKT, FALSE, 0.0, 1);


if (hTransformArg == NULL)
{
GDALClose((GDALDatasetH)
pDSrc);
GDALClose((GDALDatasetH)
pDDst);
return -3;
}

GDALWarpOptions * psWo = GDALCreateWarpOptions();

psWo->papszWarpOptions = CSLDuplicate(NULL);
psWo->eWorkingDataType = dataType;
psWo->eResampleAlg = eResample;

psWo->hSrcDS = (GDALDatasetH)
pDSrc;
psWo->hDstDS = (GDALDatasetH)
pDDst;

psWo->pfnTransformer = GDALGenImgProjTransform;
psWo->pTransformerArg = hTransformArg;

psWo->nBandCount = nBandCount;
psWo->panSrcBands = (int *)
CPLMalloc(nBandCount * sizeof(int));
psWo->panDstBands = (int *)
CPLMalloc(nBandCount * sizeof(int));
for (int i=0; i < nBandCount; i++)
{
psWo->panSrcBands[i] = i + 1;
psWo->panDstBands[i] = i + 1;
}


GDALWarpOperation
oWo;
if (oWo.Initialize(psWo) != CE_None)
{
GDALClose((GDALDatasetH)
pDSrc);
GDALClose((GDALDatasetH)
pDDst);
return -3;
}

oWo.ChunkAndWarpImage(0, 0, nNewWidth, nNewHeight);

GDALDestroyGenImgProjTransformer(hTransformArg);
GDALDestroyWarpOptions(psWo);
if (bNoGeoRef)
{
dGeoTrans[0] = dOldGeoTrans0;
pDDst->SetGeoTransform(dGeoTrans);
// pDDst->SetProjection("");
}
GDALFlushCache(pDDst);
GDALClose((GDALDatasetH)
pDSrc);
GDALClose((GDALDatasetH)
pDDst);
return 0;
}