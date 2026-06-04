# NDWI Normalized Difference Water Index — Sentinel-2 Recipe

Source: https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/ndwi/

---

# NDWI Normalized Difference Water Index

```
//VERSION 3 function setup(){return{input:[" B03 ", " B08 ", " dataMask "], output:{bands: 3}}} const ramp =[[-0.8, 0x008000],[0, 0xFFFFFF],[0.8, 0x0000CC]]; let viz = new ColorRampVisualizer(ramp); function evaluatePixel(samples){const val = index(samples. B03, samples. B08); let imgVals = viz. process(val); return imgVals. concat(samples. dataMask);}
```

```
//VERSION=3//ndwi const ramp =[[-0.8, 0x008000],[0, 0xFFFFFF],[0.8, 0x0000CC]]; let viz = new ColorRampVisualizer(ramp); function setup(){return{input:[" B03 ", " B04 ", " B08 ", " dataMask "], output:[{id: " default ", bands: 4},{id: " index ", bands: 1, sampleType: " FLOAT32 "},{id: " eobrowserStats ", bands: 2, sampleType: ' FLOAT32 '},{id: " dataMask ", bands: 1}]};} function evaluatePixel(samples){let val = index(samples. B03, samples. B08);// The library for tiffs works well only if there is only one channel returned.// So we encode the "no data" as NaN here and ignore NaNs on frontend. const indexVal = samples. dataMask === 1 ? val: NaN; let imgVals = viz. process(val); return{default: imgVals. concat(samples. dataMask), index:[indexVal], eobrowserStats:[val, isCloud(samples) ? 1: 0], dataMask:[samples. dataMask]};} function isCloud(samples){const NGDR = index(samples. B03, samples. B04); const bRatio =(samples. B03 -0.175)/(0.39 -0.175); return bRatio> 1 ||(bRatio> 0 && NGDR> 0);}
```

```
//VERSION 3 function setup(){return{input:[" B03 ", " B08 "], output:{bands: 1, sampleType: " FLOAT32 "}}} function evaluatePixel(samples){return[index(samples. B03, samples. B08)]}
```

## Evaluate and Visualize

* [Copernicus Browser](https://dataspace.copernicus.eu/browser/?zoom=11&lat=44.94637&lng=12.10183&evalscript=Ly9WRVJTSU9OPTMKLy9UaGlzIHNjcmlwdCB3YXMgY29udmVydGVkIGZyb20gdjEgdG8gdjMgdXNpbmcgdGhlIGNvbnZlcnRlciBBUEkKCi8vbmR3aQp2YXIgY29sb3JSYW1wMSA9IFsKICAJWzAsIDB4RkZGRkZGXSwKICAJWzEsIDB4MDA4MDAwXQogIF07CnZhciBjb2xvclJhbXAyID0gWwogIAlbMCwgMHhGRkZGRkZdLAogIAlbMSwgMHgwMDAwQ0NdCiAgXTsKCmxldCB2aXoxID0gbmV3IENvbG9yUmFtcFZpc3VhbGl6ZXIoY29sb3JSYW1wMSk7CmxldCB2aXoyID0gbmV3IENvbG9yUmFtcFZpc3VhbGl6ZXIoY29sb3JSYW1wMik7CgpmdW5jdGlvbiBldmFsdWF0ZVBpeGVsKHNhbXBsZXMpIHsKICB2YXIgdmFsID0gaW5kZXgoc2FtcGxlcy5CMDMsIHNhbXBsZXMuQjA4KTsKCiAgaWYgKHZhbCA8IC0wKSB7CiAgICByZXR1cm4gdml6MS5wcm9jZXNzKC12YWwpOwogIH0gZWxzZSB7CiAgICByZXR1cm4gdml6Mi5wcm9jZXNzKE1hdGguc3FydChNYXRoLnNxcnQodmFsKSkpOwogIH0KfQoKZnVuY3Rpb24gc2V0dXAoKSB7CiAgcmV0dXJuIHsKICAgIGlucHV0OiBbewogICAgICBiYW5kczogWwogICAgICAgICJCMDMiLAogICAgICAgICJCMDgiCiAgICAgIF0KICAgIH1dLAogICAgb3V0cHV0OiB7CiAgICAgIGJhbmRzOiAzCiAgICB9CiAgfQp9&datasetId=S2_L2A_CDAS&fromTime=2020-08-01T00%3A00%3A00.000Z&toTime=2020-08-01T23%3A59%3A59.999Z#custom-script)
* [EO Browser](https://apps.sentinel-hub.com/eo-browser/?zoom=11&lat=44.94637&lng=12.10183&evalscript=Ly9WRVJTSU9OPTMKLy9UaGlzIHNjcmlwdCB3YXMgY29udmVydGVkIGZyb20gdjEgdG8gdjMgdXNpbmcgdGhlIGNvbnZlcnRlciBBUEkKCi8vbmR3aQp2YXIgY29sb3JSYW1wMSA9IFsKICAJWzAsIDB4RkZGRkZGXSwKICAJWzEsIDB4MDA4MDAwXQogIF07CnZhciBjb2xvclJhbXAyID0gWwogIAlbMCwgMHhGRkZGRkZdLAogIAlbMSwgMHgwMDAwQ0NdCiAgXTsKCmxldCB2aXoxID0gbmV3IENvbG9yUmFtcFZpc3VhbGl6ZXIoY29sb3JSYW1wMSk7CmxldCB2aXoyID0gbmV3IENvbG9yUmFtcFZpc3VhbGl6ZXIoY29sb3JSYW1wMik7CgpmdW5jdGlvbiBldmFsdWF0ZVBpeGVsKHNhbXBsZXMpIHsKICB2YXIgdmFsID0gaW5kZXgoc2FtcGxlcy5CMDMsIHNhbXBsZXMuQjA4KTsKCiAgaWYgKHZhbCA8IC0wKSB7CiAgICByZXR1cm4gdml6MS5wcm9jZXNzKC12YWwpOwogIH0gZWxzZSB7CiAgICByZXR1cm4gdml6Mi5wcm9jZXNzKE1hdGguc3FydChNYXRoLnNxcnQodmFsKSkpOwogIH0KfQoKZnVuY3Rpb24gc2V0dXAoKSB7CiAgcmV0dXJuIHsKICAgIGlucHV0OiBbewogICAgICBiYW5kczogWwogICAgICAgICJCMDMiLAogICAgICAgICJCMDgiCiAgICAgIF0KICAgIH1dLAogICAgb3V0cHV0OiB7CiAgICAgIGJhbmRzOiAzCiAgICB9CiAgfQp9&datasetId=S2L2A&fromTime=2020-08-01T00%3A00%3A00.000Z&toTime=2020-08-01T23%3A59%3A59.999Z#custom-script)

## General description of the script

The NDWI is used to monitor changes related to water content in water bodies. As water bodies strongly absorb light in visible to infrared electromagnetic spectrum, NDWI uses green and near infrared bands to highlight water bodies. It is sensitive to built-up land and can result in over-estimation of water bodies. The index was proposed by McFeeters, 1996.

* Sentinel-2 NDWI = **(B03 - B08) / (B03 + B08)**
* [Landsat 1-5 MSS NDWI](https://custom-scripts.sentinel-hub.com/landsat-1-5-mss/ndwi/) = **(B01 - B04) / (B01 + B04)**
* [Landsat 4-5 TM NDWI](https://custom-scripts.sentinel-hub.com/landsat-4-5-tm/ndwi/) = **(B03 - B05) / (B03 + B05)**
* [Landsat 7 ETM+ NDWI](https://custom-scripts.sentinel-hub.com/landsat-7-etm/ndwi/) = **(B02 - B04) / (B02 + B04)**
* [Landsat 8 NDWI](https://custom-scripts.sentinel-hub.com/landsat-8/ndwi/) = **(B03 - B05) / (B03 + B05)**

Values description: Index values greater than 0.5 usually correspond to water bodies. Vegetation usually corresponds to much smaller values and built-up areas to values between zero and 0.2.

*Note: NDWI index is often used synonymously with the NDMI index, often using NIR-SWIR combination as one of the two options. NDMI seems to be consistently described using NIR-SWIR combination. As the indices with these two combinations work very differently, with NIR-SWIR highlighting differences in water content of leaves, and GREEN-NIR highlighting differences in water content of water bodies, we have decided to separate the indices on our repository as NDMI using NIR-SWIR, and NDWI using GREEN-NIR.*

## Description of representative images

NDWI of Italy. Acquired on 2020-08-01.

NDWI of Canadian lakes. Acquired on 2020-08-05.

## References

Source: https://en.wikipedia.org/wiki/Normalized\_difference\_water\_index

 

---