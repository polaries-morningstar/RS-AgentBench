# Band Combinations for Landsat 9 Imagery

Source: https://pressbooks.lib.vt.edu/remotesensing/chapter/chapter-16-band-combinations-for-landsat-9-imagery/

# Band Combinations for Landsat 9 Imagery

## Chapter 16: Band Combinations for Landsat 9 Imagery

### Introduction

This chapter discusses band combinations and how to use them within ArcGIS® Pro. We begin with a brief review of Landsat 9 spectral channels and a discussion on band combinations, spectral values for features on the surface of the Earth, and how different features can be identified using specific bands.

Each of the 11 Landsat 9 bands covers a different region of the electromagnetic spectrum. By combining three or more bands, images (outside of the visible spectrum) can be associated with red, green, and blue (RGB) colors. Remember from prior chapters discussing Landsat 9 imagery that each spectral channel (designated as a band for satellite imagery) is defined by its distinctive region of the electromagnetic spectrum. Each band is specifically tailored to help distinguish and observe specific features on the Earth's surface. See Figure 16.1 for Landsat 9 band uses. Notes at the end of this chapter provide additional details on the usefulness of individual bands and band combinations for identifying specific surface features.

Different features on the surface of the Earth respond to various wavelengths of the electromagnetic spectrum; features absorb, reflect, and re-emit the radiation in different ways. Using various band combinations to display the scene in color allows these dissimilar features to be more easily detected and identified. This process does take some experience, and users must become familiar with the scene to identify, for example, urban areas, forests, agriculture, and water bodies. Familiarity with the satellite platform (Landsat or Sentinel, for example) is vital for analyses such as unsupervised classification, supervised classification, and different indices such as NDVI.

### Using data outside the visible spectrum

Examine the tables at the end of this chapter. These tables provide several examples of how data outside the visible spectrum can be used to observe features more effectively on the Earth's surface. For example, the near-infrared (NIR) wavelengths are very useful for water bodies, as clear, calm water absorbs NIR wavelengths. Thus, water bodies appear very dark, almost black, on a color infrared image. Additionally, healthy, vigorous vegetation is more readily identified using the NIR bands, much more so than the green band. Figure 16.1 provides general information regarding the potential applications of various wavelengths of Landsat 9.

An in-depth discussion of the spectral properties of individual features on the Earth's surface is beyond the scope of this book. Additional information about this topic can be acquired from various online resources, including:

- https://www.usgs.gov/media/images/common-landsat-band-combinations
- https://earthobservatory.nasa.gov/Features/FalseColor/page6.php
- http://www.mngeo.state.mn.us/chouse/airphoto/cir.html
- https://web.pdx.edu/~nauna/resources/10_BandCombinations.htm
- https://publiclab.org/wiki/near-infrared-imaging
- https://gisgeography.com/landsat-8-bands-combinations/

Recall from Chapter 10 that when downloading scenes collected from a specific satellite platform, it is important to note that each band conveys information. Unfortunately, the band numbers' spectral properties are often inconsistent between satellite platforms (even if the band numbers are the same). For example, the spectral properties of a Band 5 image collected by Landsat 4 will not match the spectral properties of a Band 5 image collected by Landsat 9.

### Creating Different Band Combinations

This section will provide step-by-step instructions to change and explore band combinations of Landsat 9 imagery using ArcGIS® Pro.

There are several ways to assign color and change the combination of bands for a composite image.

#### Short Cut Button for Band Combinations

Select the composite image in Contents and click the Raster Layer tab. Under this tab is a button called Band Combination.

Select Band Combination. Three options are in the drop-down list-- Natural Color, Color Infrared, and Custom. Each option will be discussed, but more so as a cautionary note when using this shortcut.

Natural color uses the wavelengths of the electromagnetic spectrum in the visible range--red, green, and blue (what ArcGIS® Pro calls Bands 1, 2, 3) to display the image. Figure 16.1 depicts Band 2 as Blue (not Red), Band 3 as Green (not Blue), and Band 4 as Red. ArcGIS® Pro defaults to Red for Band 1, Green for Band 2, and Blue for Band 3. Blue is a shorter wavelength than Red, so the Blue band actually comes first in the visible range of the electromagnetic spectrum and the labeling for satellite bands. ArcGIS® Pro numbers the bands in numerical order; the band number is unrelated to the spectral properties of the bands.

Color infrared uses wavelengths from the green and red visible wavelengths and the wavelengths from the next region of the electromagnetic spectrum--near-infrared. But again, the band designations in ArcGIS® Pro do not correspond to the band sequence of Landsat 9, as Band 5 should be associated with the near-infrared band.

The third option under band combinations is Custom. Using this option, users can set a specific band combination to use regularly. When using Landsat 9 Natural Color regularly (and using all 11 bands), set the Custom parameters to Band_4 for red, Band_3 for green, and Band_2 for blue to generate a true color image. However, keep in mind that our composite image only includes seven of the eleven bands. Be careful when setting these values. Therefore, the band combination a true color image for this image is 3-2-1.

Click Add, and we have a natural color, 321 Band Combination Landsat 9 image.

---

## Single Band Sensitivities

### LANDSAT Thematic Mapper (TM & ETM+)

**0.45-0.52 μm BLUE (BAND 1)**
- Shorter wavelengths most sensitive to atmospheric haze; images may lack tonal contrast
- Longer water penetration than longer wavelengths; optimal for detecting submerged aquatic vegetation (SAV), pollution plumes, water turbidity, and sediment
- Useful for smoke plume detection (shorter wavelengths scatter more easily from smaller particles)
- Distinguishes clouds from snow and rock/soil surfaces from vegetated surfaces

**0.52-0.6 μm GREEN (BAND 2)**
- Sensitive to water turbidity differences, sediment, and pollution plumes
- Covers green reflectance peak from leaf surfaces; useful for discriminating broad vegetation classes
- Useful for SAV detection
- Useful for water penetration detecting SAV, pollution plumes, turbidity, and sediment

**0.63-0.69 μm RED (BAND 3)**
- Sensitive in strong chlorophyll absorption region; good for discriminating soil and vegetation
- Senses strong reflectance regions for most soils
- Effective for delineating soil cover

**0.76-0.9 μm NEAR IR (BAND 4)**
- Distinguishes vegetation varieties and vegetation vigor
- Water strongly absorbs NIR; good for water body delineation and distinguishing between dry and moist soils

**1.55-1.75 μm MID OR SWIR (BAND 5)**
- Sensitive to leaf-tissue water content (turgidity) changes
- Sensitive to moisture variation in vegetation and soils; reflectance decreases as water content increases
- Useful for plant vigor determination and distinguishing succulents versus woody vegetation
- Especially sensitive to ferric iron or hematite presence in rocks (reflectance increases as ferric iron increases)
- Discriminates between snow and ice (light-toned) and clouds (dark-toned)

**2.08-2.35 μm MID OR SWIR (BAND 7)**
- Coincides with hydrous mineral absorption bands (clay, mica, some oxides, and sulfates), making them appear darker; clay alteration zones associated with mineral deposits such as copper
- Useful for lithologic mapping
- Like Band 5, sensitive to moisture variation in vegetation and soils

**10.4-12.5 μm LWIR, THERMAL (BAND 6)**
- Sensor designed measuring radiant surface temperatures from -100 degrees C to +150 degrees C; day or nighttime use
- Heat mapping applications: soil moisture, rock types, thermal water plumes, household heat conservation, urban heat generation, active military targeting, wildlife inventory, geothermal detection

### Electromagnetic Spectrum and Band Coverage - Landsat 4, 5, 7, 8 and 9

Landsat 9 uses more bands relative to earlier Landsat satellite sensors. Additionally, Landsat 9's electromagnetic spectrum divisions differ from TM and ETM+ sensors aboard Landsat 4, 5, and 7. Careful band selection proves necessary when working with Landsat 9 imagery.

| Band Number | Landsat 8 & 9: Operational Land Imagers (OLI) & Thermal Infrared Sensor (TIRS) | Landsat 4 & 5: Thematic Mapper (TM) | Landsat 7: Thematic Mapper Plus (ETM+) |
|---|---|---|---|
| 1 | 0.43 - 0.45 μm - coastal aerosol | -- | -- |
| 2 | 0.45 - 0.51 μm - blue | 0.45- 0.52 μm - blue-green | -- |
| 3 | 0.53 - 0.59 μm - green | 0.52 - 0.61 μm - green | -- |
| 4 | 0.64 - 0.67 μm - red | 0.63 - 0.69 μm - red | -- |
| 5 | 0.85 - 0.88 μm - NIR | 0.76 - 0.90 μm - NIR | -- |
| 6 | 1.57 - 1.65 μm - SWIR 1 | 1.55 - 1.75 μm - SWIR | -- |
| 7 | 2.11 - 2.29 μm - SWIR 2 | 10.40 - 12.50 μm - thermal | -- |
| 8 | 0.50 - 0.68 μm - Panchromatic | 2.08 - 2.35 μm - SWIR | -- |
| 9 | 1.36 - 1.38 μm - Cirrus | 0.52 - 0.90 μm Panchromatic (ETM+ only) | -- |
| 10 | 10.60 - 11.19 μm - TIRS 1 | NONE | -- |
| 11 | 11.50 - 12.51 μm - TIRS 2 | NONE | -- |

**Definitions:**
- SWIR = Short-Wave Infrared
- Cirrus = Defined to detect and screen out contamination of cirrus clouds in other bands (not intended for analysis as separate channel)
- Coastal aerosol = Defined to analyze and estimate depths of shallow coastal waters

### Landsat Band Combination Sensitivities

#### OLI (Landsat 8 & 9)

**4-3-2**
Simulates a natural color image.

**5-6-4**
Used for the analysis of soil moisture and vegetation conditions. It is also useful for location of inland water bodies and land-water boundaries.

**5-4-3**
Known as false-color Infrared, or CIR (color infrared), this is the most conventional band combination used in remote sensing for vegetation, crops, land use, and wetlands analysis.

**7-5-3**
Analysis of soil and vegetation moisture content and location of inland water. Vegetation appears green.

**6-5-4**
Separation of urban and rural land uses; identification of land/water boundaries.

**5-6-7**
Detection of clouds, snow, and ice (in high latitudes especially).

#### TM (Landsat 4 & 5) and ETM+ (Landsat 7)

**3-2-1**
This combination simulates a natural color image. It is sometimes used for coastal studies and for detection of smoke plumes.

**4-5-3**
Used for the analysis of soil moisture and vegetation conditions. It is also useful for location of inland water bodies and land-water boundaries.

**4-3-2**
Known as false-color Infrared, this is the most conventional band combination used in remote sensing for vegetation, crops, land use, and wetlands analysis.

**7-4-2**
Analysis of soil and vegetation moisture content and location of inland water. Vegetation appears green.

**5-4-3**
Separation of urban and rural land uses; identification of land/water boundaries.

**4-5-7**
Detection of clouds, snow, and ice (in high latitudes especially).

---

## Principles of Multispectral Imaging (E-TRAINEE Course)

Source also includes content from: https://3dgeo-heidelberg.github.io/etrainee/module2/01_multispectral_principles/01_multispectral_principles.html

### Visual Interpretation of Satellite Data Concept

Image data can be analyzed based on their **resolutions**. In the context of satellite data, we consider four types of resolution: spatial, spectral, radiometric, and fixed temporal.

Starting with the visual interpretation of satellite images, they can be grouped hierarchically, with respect to the degree of complexity. At the most basic level, **tone/brightness** and **color** are the most intuitive factors for visual interpretation. Following these, spatial characteristics such as the **size**, **form (shape)**, and **texture (spatial heterogeneity)** of identified objects are considered. More complex factors include **spatial patterns** or **shadows**, which are connected with the **height** of objects. Finally, **phenology** is considered the most challenging to capture visually, since it is influenced by seasonal and interannual variations in climate.

### Spectral Ranges in the Optical Domain

Optical remote sensing is based on specific parts of the electromagnetic spectrum, particularly the wavelengths from the visible, near, and shortwave infrared ranges (approximately 0.4-2.5 micrometers). Specific wavelength ranges can be captured into separate images of the same scene, known as **bands**. Such data is referred to as **multispectral**.

The satellite multispectral data gathering process is based on three interrelated fundamental parameters: **spatial** and **spectral** resolution and **signal-to-noise (S/N) ratio**. The power level of energy in each pixel is divided into the spectral bands. The finer the spatial and spectral resolution, the less power is left to overcome the system sensor noise.

### Use of Different Ranges

Various materials have unique reflection and absorption properties of electromagnetic radiation at different wavelengths. Those different characteristics make it possible to use particular spectral ranges for their analysis and target specific phenomena. For instance **band 1** (0.43-0.45 micrometers) from Landsat 8 OLI is particularly useful for **coastal zone** observations due to the way water absorbs and reflects light in this range.

This dependence on the use of specific bands for specific analyses results from the **number of gray levels** associated with **radiometric** resolution of the data and **brightness** of particular pixels. The greater the variation in the brightness of pixels representing different objects - the more useful the band for analysis. However, the human eye is more sensitive to color variations than brightness variations, which is why **color (multiband) compositions** are often used in the visual interpretation of satellite images.

Plotting three selected spectral bands together allows for the creation of an **RGB image composition**. While our eyes are most accustomed to compositions based on red, green, and blue bands, the availability of near and shortwave infrared bands allows us to create false color images. Such compositions allow for better discrimination of e.g. deciduous/coniferous forests, healthy/damaged vegetation, and so on.

In multispectral data, the number of bands and their width are crucial factors. Generally, this type of data includes 3 to 10 discrete and rather broad bands (distinguishing them from hyperspectral data, which can include hundreds of very narrow bands).

### Spectral Indices

Different spectral bands allow for creating their combinations called **spectral indices**: mathematical measures that compare the spectral reflection in more than one spectral band.

For multispectral data analysis, both broadband and narrowband indices can be calculated, depending on the sensor used.

Spectral indices can be dedicated to various objects and their characteristics. Due to the great dynamics of the changes taking place, most indices are related to **vegetation**. There are also indices developed for studying topics such as **snow cover**, **built-up areas**, **rocks and minerals**, and **fire/burnt areas**.

**Normalized Difference Vegetation Index** (NDVI) is one of the most common vegetation indices, which provides a measure of the general condition of vegetation and biomass.

**Selected Vegetation Indices Formulas:**

| Index | General Formula | Landsat 5-7 | Landsat 8-9 | Sentinel-2 |
|-------|-----------------|-------------|-------------|------------|
| NDVI | NIR-RED/NIR+RED | B4-B3/B4+B3 | B5-B4/B5+B4 | B8-B4/B8+B4 |
| NDMI | NIR-SWIR/NIR+SWIR | B4-B5/B4+B5 | B5-B6/B5+B6 | B8-B11/B8+B11 |
| NPCI | RED-BLUE/RED+BLUE | B3-B1/B3+B1 | B4-B2/B4+B2 | B4-B2/B4+B2 |
| NBR | NIR-SWIR/NIR+SWIR | B4-B7/B4+B7 | B5-B7/B5+B7 | B8-B12/B8+B12 |

### Selected Sensor Characteristics

**Table: Selected Satellite Sensor Characteristics**

| Satellite | Sensor | Spectral Range (µm) | Pixel Size (m) | Swath Width (km) |
|-----------|--------|---------------------|----------------|------------------|
| Aqua | MODIS | VNIR+SWIR (0.40-2.155), TIR (3.66-14.28) | 250-1000 | 2330 |
| Landsat 4/5 | Thematic Mapper (TM) | VNIR+SWIR (0.45-2.35) | 30 | 185 |
| Landsat 7 | ETM+ | PAN (0.52-0.90), VNIR+SWIR (0.45-2.35), TIR (10.40-12.50) | 15/30/60 | 185 |
| Landsat 8 | OLI/TIRS | PAN (0.50-0.68), VNIR+SWIR (0.43-2.29), TIR (10.60-12.51) | 15/30/100 | 185 |
| Landsat 9 | OLI2 | PAN (0.50-0.68), VNIR+SWIR (0.43-2.29), TIR (10.30-12.50) | 15/30/100 | 185 |
| Pleiades-1 | HiRI | PAN (0.47-0.83), VNIR (0.43-0.94) | 0.5/2 | 20 |
| PlanetScope | PS2 | VNIR (0.45-0.86) | 3 | 24 |
| Sentinel-2 | MSI | VNIR+SWIR (0.44-2.20) | 10-60 | 290 |
| WorldView-2 | WV110 | PAN (0.45-0.80), VNIR (0.40-1.04) | 0.46/1.8 | 16.4 |
| WorldView-3 | WV110 | PAN (0.45-0.80), VNIR+SWIR (0.40-2.36) | 0.31/1.24-3.70 | 13.1 |
