# Radiometric Corrections in Remote Sensing

Source: https://geolearn.in/radiometric-correction/
Source: http://gsp.humboldt.edu/olm/Courses/GSP_216/online/lesson7/radiometric.html
Source: https://cwcaribbean.aoml.noaa.gov/bilko/module7/lesson3/

# Radiometric Corrections in Remote Sensing: Why it is Essential for Accurate Analysis

Published: June 25, 2023 by Geolearn

**Introduction:**

Remote sensing is the science of acquiring information about the Earth's surface without physical contact. It involves the use of sensors that detect and measure the electromagnetic radiation emitted or reflected from the Earth's surface. One of the most critical factors in remote sensing is radiometric correction, which is the process of correcting the digital numbers (DNs) recorded by a sensor to remove any systematic errors or inconsistencies in the data caused by various factors.

Radiometric corrections are necessary because the digital numbers recorded by remote sensing sensors are not absolute measurements of the reflected or emitted radiation from the Earth's surface. Rather, they are relative measurements that are influenced by a variety of factors, such as the characteristics of the sensor, the atmosphere, and the Earth's surface. For example, the DN values recorded by a sensor may be affected by variations in the amount of solar radiation, atmospheric absorption and scattering, surface reflectance, and sensor noise. These factors can cause the DN values to vary over time, space, and spectral bands, which can make it difficult to compare and analyze remote sensing data.

Radiometric corrections are essential to ensure the accuracy and reliability of remote sensing data for various applications, such as land cover classification, vegetation monitoring, and climate change studies. They involve the application of correction factors to the DN values to remove the systematic errors or inconsistencies caused by the factors mentioned above. The goal of radiometric correction is to convert the raw DN values into calibrated reflectance or radiance values, which are absolute measurements of the radiation that can be compared and analyzed across different sensors, times, and spectral bands.

Several types of radiometric corrections can be applied to remote sensing data. These include:

### **Sensor Calibration:**

This correction involves the calibration of the sensor to remove any systematic errors in the sensor's response to radiation. Sensor calibration is typically performed before or after the acquisition of the remote sensing data.

### **Atmospheric correction:**

This correction involves the removal of the atmospheric effects on the radiation recorded by the sensor. The atmosphere can cause the radiation to scatter or absorb, which can affect the DN values recorded by the sensor. Atmospheric correction involves the use of atmospheric models and correction algorithms to estimate and remove atmospheric effects.

Bidirectional reflectance distribution function (BRDF) correction: This correction involves the normalization of the DN values to account for the directionality of the reflected radiation from the Earth's surface. BRDF correction is essential for comparing the reflectance values across different illumination and viewing geometries.

### **Noise Reduction:**

This correction involves the removal of the sensor noise from the DN values to improve the signal-to-noise ratio of the remote sensing data.

The methods for radiometric correction vary depending on the type of correction and the characteristics of the data. Some of the commonly used methods include:

### **Empirical Line Method:**

This method involves the use of ground-based measurements of reflectance or radiance to calibrate the sensor's response to radiation. The method assumes a linear relationship between the DN values and the ground-based measurements.

### **Dark object subtraction:**

This method involves the use of dark objects, such as shadows or water bodies, to estimate the minimum DN value that should correspond to zero reflectance or radiance.

### **Look-up Tables**:

This method involves the use of pre-calibrated look-up tables that relate the DN values to the calibrated reflectance or radiance values.

### **Cross Calibration:**

This method involves the comparison of the remote sensing data acquired by different sensors that have overlapping spectral bands to estimate the correction factors.

Radiometric corrections are not without challenges and limitations. Some of the challenges include the availability and quality of ground-based measurements, the environmental variability of the Earth's surface, and the complexity of the correction algorithms.

**Importance of Radiometric Corrections in Remote Sensing**

Radiometric corrections are essential in remote sensing for a variety of reasons. Some of the major significance of radiometric corrections are:

### **Accurate Image Interpretation:**

Radiometric corrections help in achieving accurate image interpretation by correcting for errors and variations in the radiometric values of the remotely sensed data. These corrections ensure that the true reflectance values of the objects on the ground are captured and that the image is free from any distortions.

### **Better Image Enhancement:**

Radiometric corrections enable better image enhancement by ensuring that the data is normalized and calibrated. This makes it easier to perform various image enhancement techniques, such as contrast stretching, histogram equalization, and sharpening, which can improve the visibility and detail of the image.

### **Consistent Data Analysis:**

Radiometric corrections ensure that the remotely sensed data is consistent across different images, sensors, and platforms. This is particularly important for time-series analysis, where consistent data is required to monitor changes in the environment over time.

### **Better Quantitative Analysis:**

Radiometric corrections allow for better quantitative analysis by providing accurate radiometric values of the objects on the ground. This enables the estimation of various parameters, such as vegetation indices, surface temperature, and land cover classification, which are essential for environmental monitoring and management.

### **Improved Data Fusion:**

Radiometric corrections enable the fusion of data from different sensors and platforms, as they ensure that the radiometric values are consistent and compatible. This allows for the integration of different data sources, such as optical, thermal, and radar data, which can provide a more comprehensive understanding of the environment.

### **Interoperability:**

Radiometrically corrected data become more interoperable, which can be combined with other datasets or integrated into geographic information systems (GIS) for further analysis and decision-making. This interoperability enhances the usefulness and applicability of remote-sensing data in various domains.

### **Data Normalization:**

By converting DN values to radiance or reflectance, radiometric corrections normalize the data, enabling meaningful comparisons across different images and sensors. This normalization facilitates change detection, land cover classification, and other quantitative analyses.

**Need of Radiometric Corrections in the Remote Sensing Process**

The primary objective of radiometric corrections is to convert the acquired raw digital numbers (DN) into physically meaningful units such as radiance or reflectance. This conversion is crucial because DN values are arbitrary and can vary between sensors, acquisitions, and platforms, making it difficult to compare and analyze data consistently. By converting DN values to radiance or reflectance, radiometric corrections allow for quantitative measurements and meaningful comparisons across different images and sensors.

**Several factors contribute to the need for radiometric corrections:**

1. **Sensor Characteristics:**

Remote sensing sensors have inherent limitations and characteristics that can introduce distortions in the acquired data. These include sensor-specific noise, calibration errors, and variations in the sensor's response to different wavelengths. Radiometric corrections account for these sensor-specific effects to ensure data consistency.

2. **Atmospheric Effects:**

The Earth's atmosphere interacts with the incoming electromagnetic radiation, leading to scattering, absorption, and other phenomena. These atmospheric effects can distort the recorded signals, particularly in the visible and near-infrared regions. Radiometric corrections incorporate atmospheric correction algorithms to remove or minimize these effects, allowing for an accurate interpretation of surface properties.

3. **Sun-sensor Geometry:**

The angle of the sun, as well as the viewing geometry of the sensor, can affect the amount of radiation received by the sensor. Changes in the sun-sensor geometry during image acquisition can result in variations in the recorded signal intensities. Radiometric corrections account for these geometric effects, ensuring that data from different times and locations are comparable.

**Challenges and Limitations of Radiometric Corrections**

Radiometric corrections are a critical component of remote sensing analysis, but they come with their own set of challenges and limitations. Here are some of the major challenges and limitations associated with radiometric corrections:

### **Atmospheric effects:**

The atmosphere can affect the radiometric properties of remotely sensed data. Aerosols, water vapor, and other atmospheric constituents can scatter, absorb, and reflect radiation, leading to errors in radiometric calibration. Several atmospheric correction models have been developed to mitigate this problem.

### **Topographic effects:**

Terrain slopes and aspects can also affect the radiometric properties of remotely sensed data. This is because different areas of a slope receive different amounts of sunlight, leading to variations in reflectance. Topographic corrections are typically performed to account for these effects.

### **Sensor noise:**

All sensors have some level of noise or error associated with their measurements. Radiometric corrections can reduce some of this noise, but it is not always possible to eliminate it.

### **Spectral calibration:**

Radiometric corrections assume that the spectral response of the sensor is stable over time. However, the spectral response can change due to aging, temperature, or other factors. This can lead to errors in radiometric calibration if not accounted for.

### **Saturation effects:**

When the sensor collects too much radiation, the signal becomes saturated, and data can be lost. This can occur when the sensor is pointed at bright objects or areas with high reflectance. Radiometric corrections can help mitigate this issue by adjusting the sensor's gain or exposure time.

### **Data storage and processing limitations:**

Radiometric corrections can be computationally intensive and require significant storage capacity. Large datasets can be difficult to manage, and it may not always be feasible to store or process all the data. Despite these challenges and limitations, radiometric corrections remain an essential part of remote sensing analysis. By reducing noise and correcting for atmospheric and topographic effects, radiometric corrections can improve the accuracy and precision of remotely sensed data, leading to better-informed decision-making.

---

# Radiometric Calibration and Corrections

Source: http://gsp.humboldt.edu/olm/Courses/GSP_216/online/lesson7/radiometric.html

## Introduction

Radiometric correction is done to calibrate the pixel values and/ correct for errors in the values. The process improves the interpretability and quality of remote sensed data. Radiometric calibration and corrections are particularly important when comparing multiple data sets over a period of time.

The energy that sensors on aircraft or satellites record can differ from the actual energy emitted or reflected from a surface on the ground. This is due to the sun's azimuth and elevation and atmospheric conditions that can influence the energy observed by the sensor. Therefore, in order to obtain the real or true ground radiance or reflectance values, radiometric errors must be accounted for.

The figure above depicts the atmospheric effects that influence the measurement of reflected energy by remote sensors. this include path radiance from atmospheric scattering and the reduction of the total irradiance.

The radiance detected or measured by satellite based sensors includes the reflected radiation from the Earth's surface as well as radiation that is scattered by particles in the atmosphere. Nearly all energy recorded by sensors is affected by the atmosphere to some extent. The atmosphere influences the radiance in two opposite ways. First, it can scatter light, adding to the radiation or radiance that is detected by the sensor. This is known as _path radiance._ Second, it can reduce reduce the energy that illuminates the surface, known as incident radiation or irradiation. The irradiance varies on the time of the year due to seasonal differences in the solar elevation and the distance between the Earth and the Sun. The atmospheric effects are also influenced by the wavelength. For example, Rayleigh scattering is more pronounced at shorter wavelengths.

## Radiometric Correction and Calibration

The value recorded for a given pixel includes not only the reflected or emitted radiation from the surface, but also the radiation scattered and emitted by the atmosphere. In most cases we are interested in only the actual surface values. To achieve these values, radiometric calibration and correction processes must be applied.

### Radiometric Calibration

A sensor records the intensity of the electromagnetic radiation for each pixel as a digital number (DN). For many sensors, these digital numbers can be converted to more meaningful real world units like radiance, reflectance or brightness temperature. Sensor specific information is needed to carry out this calibration process. In the case of Landsat data, the metadata file contains the necessary information. Most image processing software packages have radiometric calibration tools. In ENVI Landsat data can be converted directly to reflectance, without needing to first calculate radiance.

#### Converting DNs to Radiance and Reflectance

The raw digital numbers (DN) in the images like Landsat can be converted to what is known as top-of-atmosphere (TOA) radiance or reflectance. Equations rescale the data based on sensor specific information and remove the effects of differences in illumination geometry (different solar angle, Earth-sun distance). Most remote sensing software packages have tools to calibrate the data.

#### Converting to At-Satellite Brightness Temperature

Similar to reflectance values, data from many thermal sensors can be converted to what is known as a Brightness Temperature. The brightness temperature is a temperature that is obtained by measure the emitted radiance of a surface. The brightness temperature is usually expressed in Kelvin (K). For Landsat 8 Thermal Infrared Sensor (TIRS) the at-satellite brightness temperature can be calculated using the thermal constant that is provided in the metadata file.

### Atmospheric Correction

Atmospheric correction is the process of removing the effects of the atmosphere to produce surface reflectance values. Atmospheric correction can significantly improve the interpretability and use of an image. Ideally, this process requires knowledge of the atmospheric conditions and aerosol properties at the time the image was acquired.

#### Atmospheric Correction Models

Atmospheric models can be used to account for the effects of scattering and absorption in the atmosphere. A number of parameters are required to accurately apply atmospheric correction, including properties such as the amount of water vapor, distribution of aerosols. Sometimes this data can be collected by field instruments that measure atmospheric gases and aerosols, but this is often expensive and time consuming. Other satellite data can also be used to help estimate the amount and distribution of atmospheric aerosols. Many software packages include special atmospheric correction modules that use atmospheric radiation transfer models to produce an estimate of the true surface reflectance.

#### Dark Object Subtraction Method

This method is used when there is no available data on atmospheric conditions and aerosol properties at the time the image was acquired. The basic assumption of this method is that within the image some pixels are in complete shadow and their radiances received at the satellite are due entirely to atmospheric scattering (path radiance). This path radiance value is then subtracting from each pixel value in the image. The accuracy of these techniques are generally lower than physically-based corrections, but they are useful when no atmospheric measurements are available.

## Landsat Land Surface Reflectance Products

Recently the USGS has developed software to apply calibration and atmospheric correction routines to Landsat level 1 data products. This data is known as **Surface Reflectance Higher-Level data** or **Level 2 Data** and is available for Landsat 4-5 Thematic Mapper (TM), Landsat 7 Enhanced Thematic Mapper Plus (ETM+) and Landsat 8 Operational Land Imager (OLI) data. These data products have been radiometrically calibrated and atmospherically corrected using specialized algorithms. They are designed to monitor and asses changes in the land over time. These data products can be ordered through EarthExplorer under the Landsat: Collection 1 Level-2 (On-Demand). You will have to order the Surface Reflectance data, but there is no charge. Typically data is available for download within 24 hours of ordering.

---

# Bilko Module 7 - Radiometric correction of satellite images
# Source: https://cwcaribbean.aoml.noaa.gov/bilko/module7/lesson3/

## Step 1. Conversion of DN to spectral radiance

This is a fairly straightforward process which requires information on the gain and bias of the sensor in each band. The transformation is based on a calibration curve of DN to radiance which has been calculated by the operators of the satellite system. The calibration is carried out before the sensor is launched and the accuracy declines as the sensitivity of the sensor changes over time. Periodically attempts are made to re-calibrate the sensor.

## Step 2. Conversion of spectral radiance to exoatmospheric reflectance

The apparent reflectance, which for satellite images is termed exoatmospheric reflectance, r, relates the measured radiance, L (which is what the formulae above will output), to the solar irradiance incident at the top of the atmosphere and is expressed as a decimal fraction between 0 and 1.

r = unitless planetary reflectance at the satellite (this takes values of 0-1.)

## Step 3. Removal of atmospheric effects due to absorption and scattering

A detailed discussion of the methods available for atmospheric correction is available in Kaufman (1989). Atmospheric correction techniques can be broadly split into three groups: Removal of path radiance (e.g. dark pixel subtraction which will be carried out in Lesson 4), Radiance-reflectance conversion, and Atmospheric modelling (e.g. 5S radiative transfer code, which will be used here). Atmospheric modelling is perhaps the most sophisticated method used to compensate for atmospheric absorption and scattering. Ideally, modelling approaches are best used when scene-specific atmospheric data are available (e.g. aerosol content, atmospheric visibility). However, such information is rarely available.
