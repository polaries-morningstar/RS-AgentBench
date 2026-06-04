# Remote Sensing Fundamentals

Source: https://www.earthdata.nasa.gov/learn/backgrounders/remote-sensing

# Earth Observation Data Basics

"The life cycle of Earth observation data is rich and complex, with many points of entry along the pipeline. From collection to visualization, we dive deep into the basics to demystify the incredible data in our catalog."

## Remote Sensing

"Remote sensing is the acquiring of information from a distance. NASA observes Earth and other planetary bodies via remote instruments on space-based platforms (e.g., satellites or spacecraft) and on aircraft that detect and record reflected or emitted energy. Remote instruments, which provide a global perspective and a wealth of data about Earth systems, enable data-informed decision making based on the current and future state of our planet."

For detailed training, the Applied Remote Sensing Training (ARSET) program offers a Fundamentals of Remote Sensing course.

## Remote Sensing Data Basics

### Orbits

"An orbit is the curved path a satellite follows around the Earth due to gravitational force."

### Resolution

"There are four types of resolution to consider for any dataset--radiometric, spatial, spectral, and temporal. Resolution plays a role in how data from a instrument can be used. Resolution can vary depending on the platform's orbit and instrument design."

- **Radiometric**: "the amount of information in each pixel, that is, the number of bits representing the energy recorded."
- **Spatial**: "Spatial resolution is the Horizontal Data Resolution which describes the resolution of data that has been georeferenced to a geodetic datum, and is defined as the smallest horizontal distance between successive elements of data in a dataset."
- **Spectral**: "the ability of an instrument to discern finer wavelengths, that is, having more and narrower bands."
- **Temporal**: "Temporal resolution is the time it takes for a space-based platform to complete an orbit and revisit the same observation area. Temporal resolution depends on the orbit, the instrument's characteristics, and the swath width."

### The Electromagnetic Spectrum

"To understand remotely sensed data, it is imperative to know the electromagnetic spectrum."

### Active Instruments

"Active instruments emit energy and collect data based on changes in the return signal."

### Passive Instruments

"Passive instruments detect energy emitted from the natural environment."

### Essential Variables

"Essential variables are known to be critical for observing and monitoring a given facet of the Earth system."

### Data Processing, Interpretation, and Analysis

"Remote sensing data acquired from instruments aboard satellites require processing before the data are usable by most researchers and applied science users."

## Understanding Metadata

"This interactive tool helps users navigate and understand essential metadata on our Earth science dataset landing pages. Through guided examples and hands-on exploration, learn critical context about our data to aid you in your own scientific discoveries."

### Parts of Earthdata Dataset Landing Pages

**Long Name/Entry Title**: "This element describes the title of the dataset. Long Name is synonymous with Entry Title."

**Short Name**: "The Short Name is an abbreviated name for a dataset."

**Version**: "Version is used to distinguish between versions of a given data product (e.g., produced using different processing algorithms or updates to calibration parameters). It is encouraged to use the latest version of a data product."

**Digital Object Identifier (DOI)**: "The Digital Object Identifier (DOI) is a persistent identifier that is used to uniquely identify objects including datasets and documents. The DOI field also includes the option to provide information on the authority that registers the DOI, as well as the DOI of the previous version of the record."

**Center/Project**: "This is the data provider for the data collection."

**Cloud Icon**: "The cloud icon indicates the dataset lives in the cloud as opposed to on-premises. Clicking on the icon shows the Concept ID for the dataset."

**Data Alert Icon**: "If the dataset has any data alerts (active outage, resolved outage, data update, data release, or retired dataset alert), the alert icon will show. Click on the icon to see the alerts logged."

**Copy URL/Copy API Command**: "Click on the vertical ellipses for the option to copy the dataset landing page URL, the metadata URL from CMR (copy API command), and there are also a few buttons for sharing the dataset to social media."

**Data Format**: "A standard way that information is encoded for storage in a computer file (learn more about data formats)."

**Dataset Size**: "This is a unit of measure for the total collection file size (e.g., KB, MB, TB)."

**Spatial Extent**: "The Spatial Extent element describes the geographic coverage of the data. At the collection-level, the spatial extent describes the area of the Earth that a data product covers as a whole. For specific files or granules, the spatial extent describes the area covered by that individual file."

**Spatial Resolution**: "Spatial resolution is the Horizontal Data Resolution which describes the resolution of data that has been georeferenced to a geodetic datum, and is defined as the smallest horizontal distance between successive elements of data in a dataset."

**Temporal Extent**: "Temporal Extent describes when data were acquired or collected."

**Documents and Resources**: "This is where you will find the documents related to the data collection (User Guide, Algorithm Theoretical Basis Document (ATBD)) and learning resources that use the data collection."

**Publications**: "This is a list of publications that cite the data collection."

**Variables**: "Variables are a set of physical properties whose values determine the characteristics or behavior of something. For example, temperature and pressure are variables of the atmosphere. Parameters and variables can be used interchangeably. Variable level attributes provide individual information for each variable."

**Platforms**: "The platform is used to collect the data available in the dataset."

**Instruments**: "The instrument is used to collect the data available in the dataset."

**Coordinate System**: "Cartesian and Geodetic are the choices to display for coordinate system in the metadata. Cartesian refers to a grid that helps us pinpoint exactly where something is located. Think of perpendicular axes (x-axis and y-axis in 2-dimensional) that intersect at the origin (0,0) to define locations (coordinates) for points in space. Geodetic coordinates account for the curve of the Earth and typically use latitude (north/south), longitude (east/west), and height above sea level to pinpoint locations."

**Granule Spatial Representation**: "The same definition as Coordinate System above except on a smaller scale since a granule is one part or chunk of a data collection."

**Temporal Resolution**: "Temporal resolution is the time it takes for a space-based platform to complete an orbit and revisit the same observation area. Temporal resolution depends on the orbit, the instrument's characteristics, and the swath width."

**Concept ID**: "This is another unique identifier for a data collection in the Common Metadata Repository (CMR)."

**Data State**: "The Collection Progress or Data State describes the production status of the dataset. The Collection Progress element leverages a controlled vocabulary to ensure consistency across data collections."

**Number of Files/Granules**: "This number indicates how many files or granules are in a data collection."

**Processing Level**: "An identifier indicating the level at which the data in the collection are processed, ranging from level 0 (raw instrument data at full resolution) to level 4 (model output or analysis results)."

**Science Keywords**: "Science Keywords are synonymous with Topics and Science Disciplines. Related science keywords are selected by the metadata curator based on the Global Change Master Directory and relate the data collection to potential application areas, resources, and other related information."

**Citation**: "The citation information is provided for data users to easily cite the data used in their publications."

**File Naming Convention**: "The File Naming Convention refers to the naming convention of the data set's (Collection's) data files along with a description of the granule file construction."

## Technology

"Innovations in artificial intelligence, climate models, and cloud computing are improving the ways users work with Earth science data, especially massive datasets like those expected from NISAR. NASA leverages modern computing approaches to optimize the quality of data collected and the speed at which users are able to drill down to the details they need to support on-the-ground science."

### Cloud Computing

"Nearly all of NASA's Earth science data is accessible through Earthdata Cloud, making access, analysis, and visualization more efficient and cost effective. We offer resources including Python libraries, tutorials, and data recipes to help users optimize working with data in the cloud."

### Earth Observation Data and Artificial Intelligence

"The application of artificial intelligence (AI) to Earth science data makes it possible to search through large amounts of data to find relationships."

## Synthetic Aperture Radar

"Synthetic aperture radar (SAR) is a type of remote sensing that produces fine-resolution data using a technology that, over time, can detect even minute changes on Earth's surface."

**Synthetic Aperture Radar (SAR)**: "SAR is one of the power technologies of remote sensing, and enables high resolution imagery to be created night or day, regardless of weather conditions."

**The SAR Handbook**: "The SAR Handbook was created in 2019 as a guide for forest monitoring and biomass estimation with synthetic aperture radar (SAR)."

**Types of SAR Products**: "View a table of synthetic aperture radar (SAR) products and their processing levels available through NASA's Earth Science Data Systems (ESDS) Program."

**SAR Image Interpretation**: "General rules of thumb for interpreting synthetic aperture radar (SAR) imagery and resources for viewing SAR imagery."

## Glossary of Terms

"Reference the Earth Observation Data Basics Glossary to better understand terms related to the data provided by our program."

**Acquisition Strategy Meeting (ASM)**: "An ASM is a forum where senior Agency management reviews major acquisitions in programs and projects before authorizing significant budget expenditures. The ASM is held at the Mission Directorate/Mission Support Office level, implementing the decisions that flow out of the earlier Agency acquisition strategy planning. The ASM is typically held early in Formulation, but the timing is determined by the Mission Directorate. The ASM focuses on considerations such as impacting the Agency workforce, maintaining core capabilities and make-or-buy planning, and supporting Center assignments and potential partners."

**Aerosols**: "A gaseous suspension of fine solid or liquid particles that can travel vast distances form their original source, affecting air quality and visibility."

**Albedo**: "The ratio of radiation reflected by a surface compared to the amount it receives."

**Algorithm**: "A formula or set of steps used, sometimes repetitively, to solve a problem. Algorithms implemented as software are delivered to NASA's Science Investigator-led Processing System (SIPS) or to NASA's Science Data Processing Segment (SDPS) by a science investigator (principal investigator, team leader, or Interdisciplinary Investigator) to use as primary tools in the generation of science products. The term includes executable code, source code, job control scripts, and documentation."

**Algorithm Theoretical Basis Document (ATBD)**: "An ATBD describes the physical and mathematical description of the algorithms to be used in the generation of data products. It includes a description of variance and uncertainty estimates and considerations of calibration and validation, exception control, and diagnostics. In some cases, internal and external data product flows are required."

**Ancillary Data**: "Data which are not obtained from the sensor itself (usually provided in the science telemetry) and have the primary purpose to serve the processing of instrument data. This can be divided into data referred to as spacecraft 'engineering', 'core housekeeping' or 'subsystem' data obtained from other parts of the platform and includes parameters such as orbit position and velocity, attitude and its range of change, time, temperatures, pressures, jet firings, water dumps, internally produced magnet fields, and other environmental measurements. Ancillary refers to data that exist purely to serve the data processing; auxiliary data, while helping the process, are also data sets in their own right."

**Apogee**: "The farthest point of an elliptical orbit. For an Earth-centered orbit, this is the point where the orbiting body is farthest from the center of the Earth."

**Application Programming Interface (API)**: "A system access point or library function that has a well-defined syntax and is accessible from application programs or user code to provide well-defined functionality."

**Archive**: "The archive stores data products, guaranteeing their preservation for future use. This function includes all operations to identify, store and retrieve the data and ensure their integrity."

**Attitude Data**: "Data that represent spacecraft orientation and onboard pointing information. Attitude data includes: attitude sensor data used to determine the pointing of the spacecraft axes, calibration and alignment data, Euler angles or quaternions, rates and biases, and associated parameters. Attitude generated onboard in quaternion or Euler angle form. Refined and routine production data related to the accuracy or knowledge of the attitude."

**Attribute**: "An element of metadata, e.g., title, summary, format, dataset language."

**Big Data**: "Big data is a broad term for data sets so large or complex that traditional data processing applications are inadequate. Challenges include analysis, capture, data curation, search, sharing, storage, transfer, visualization, querying and information privacy."

**Browse Image**: "Visual representation of a product (as an image) to help and support product selection in the frame of the user service facility. Synonyms are: Browse, Quick-look, and Preview."

**Calibration**: "The process of quantitatively defining the system responses to known, controlled signal inputs."

**Calibration Data**: "The collection of data required to perform calibration of the instrument science data, instrument engineering data, and the spacecraft or platform engineering data. It includes pre-flight and in-flight calibration measurements, calibration equation coefficients derived from calibration software routines, and ground truth data that is to be used in the data calibration processing routine."

**Campaign**: "An observational study used to acquire targeted observations or samples to support a clearly defined science or research objectives. Also called (or at least related to) what some stakeholders call a Mission, Project, Field Campaign, or Field Investigation. A campaign may be a multi-year program with multiple projects, such as the Arctic-Boreal Vulnerability Experiment (ABoVE), an Earth Ventures Suborbital (EVS) mission, such as Delta-X, or a single project targeting a specific set of measurements, such as the CARbon Atmospheric Flux Experiment (CARAFE)."

**Clouds**: "A visible aggregate of minute water droplets and/or ice crystals in the atmosphere above the Earth's surface."

**Collection or aggregate metadata**: "These are metadata elements that describe an entire set of data products or files. Values of collection metadata apply to all of the products in a specific collection. Collections may represent the same release of any given data product, sets of data generated during an experiment, a campaign or an algorithmic test."

**Data**: "Scientific or technical measurements, values calculated therefrom, observations, or facts that can be represented by numbers, tables, graphs, models, text, or symbols which are used as a basis for reasoning and further calculation. For NASA's Earth Science Program and according to NASA's Earth Science Data & Information Policy, the term 'data' includes observation data, metadata, products, information, algorithms, including scientific source code, documentation, models, images, and research results."

**Data Assimilation**: "Data assimilation is defined as the process of combining observations with model simulations to enhance the accuracy of predictions."

**Data Collection**: "A major release of a data product, or of a set of closely related data products, which can be followed by minor releases within the same collection."

**Data Format**: "A standard way that information is encoded for storage in a computer file. An example is HDF5."

**Data Management**: "As defined for an OAIS entity that contains the services and functions for populating, maintaining, and accessing a wide variety of information. Some examples of this information are catalogs and inventories on what may be retrieved from Archival Storage, processing algorithms that may be run on retrieved data, Consumer access statistics, Consumer billing, Event Based Orders, security controls, and OAIS schedules, policies, and procedures."

**Data Processing Level**: "The level of processing that results in data products ranging from raw instrument data to refined analyses that use inputs from various sources."

**Data Product**: "A set of data files that can contain multiple parameters and that compose a logically meaningful group of related data."

**Data User Guide**: "A document, either on-line or hardcopy, containing the necessary information for the correct usage of the data."

**Derived Products**: "Derived products are higher level products (level 1b through 4) where calibration and geo-location transformations have been applied to generate sensor units, and/or algorithms have been applied to generate gridded geophysical parameters."

**Directory**: "A collection of uniform descriptions that summarize the contents of a large number of data sets. It provides information suitable for making an initial determination of the existence and contents of each data set."

---

# Source: https://crisp.nus.edu.sg/~research/tutorial/em.htm

## Electromagnetic Waves

Electromagnetic waves are energy transported through space in the form of periodic disturbances of electric and magnetic fields. All electromagnetic waves travel through space at the same speed, c = 2.99792458 x 10⁸ m/s, commonly known as the speed of light. An electromagnetic wave is characterized by a frequency and a wavelength. These two quantities are related to the speed of light by the equation,
speed of light = frequency x wavelength

The frequency (and hence, the wavelength) of an electromagnetic wave depends on its source. There is a wide range of frequency encountered in our physical world, ranging from the low frequency of the electric waves generated by the power transmission lines to the very high frequency of the gamma rays originating from the atomic nuclei. This wide frequency range of electromagnetic waves constitute the Electromagnetic Spectrum.

## The Electromagnetic Spectrum

The electromagnetic spectrum can be divided into several wavelength (frequency) regions, among which only a narrow band from about 400 to 700 nm is visible to the human eyes. Note that there is no sharp boundary between these regions. The boundaries shown in the above figures are approximate and there are overlaps between two adjacent regions.

Wavelength units: 1 mm = 1000 µm; 1 µm = 1000 nm.

Radio Waves: 10 cm to 10 km wavelength.

Microwaves: 1 mm to 1 m wavelength.
The microwaves are further divided into different frequency (wavelength) bands:
(1 GHz = 10⁹ Hz)
- P band: 0.3 - 1 GHz (30 - 100 cm)
- L band: 1 - 2 GHz (15 - 30 cm)
- S band: 2 - 4 GHz (7.5 - 15 cm)
- C band: 4 - 8 GHz (3.8 - 7.5 cm)
- X band: 8 - 12.5 GHz (2.4 - 3.8 cm)
- Ku band: 12.5 - 18 GHz (1.7 - 2.4 cm)
- K band: 18 - 26.5 GHz (1.1 - 1.7 cm)
- Ka band: 26.5 - 40 GHz (0.75 - 1.1 cm)

Infrared: 0.7 to 300 µm wavelength.
This region is further divided into the following bands:
- Near Infrared (NIR): 0.7 to 1.5 µm.
- Short Wavelength Infrared (SWIR): 1.5 to 3 µm.
- Mid Wavelength Infrared (MWIR): 3 to 8 µm.
- Long Wavelength Infrared (LWIR): 8 to 15 µm.
- Far Infrared (FIR): longer than 15 µm.

The NIR and SWIR are also known as the Reflected Infrared, referring to the main infrared component of the solar radiation reflected from the earth's surface. The MWIR and LWIR are the Thermal Infrared.

Visible Light: This narrow band of electromagnetic radiation extends from about 400 nm (violet) to about 700 nm (red). The various colour components of the visible spectrum fall roughly within the following wavelength regions:
- Red: 610 - 700 nm
- Orange: 590 - 610 nm
- Yellow: 570 - 590 nm
- Green: 500 - 570 nm
- Blue: 450 - 500 nm
- Indigo: 430 - 450 nm
- Violet: 400 - 430 nm

Ultraviolet: 3 to 400 nm

X-Rays and Gamma Rays

## Photons

According to quantum physics, the energy of an electromagnetic wave is quantized, i.e. it can only exist in discrete amount. The basic unit of energy for an electromagnetic wave is called a photon. The energy E of a photon is proportional to the wave frequency f,
E = hf
where the constant of proportionality h is the Planck's Constant,
h = 6.626 x 10⁻³⁴ J s.

---

# Source: https://en.wikipedia.org/wiki/Remote_sensing

Remote sensing is the acquisition of information about an object or phenomenon without making physical contact with the object, in contrast to in situ or on-site observation. The term is applied especially to acquiring information about Earth and other planets. Remote sensing is used in numerous fields, including geophysics, geography, land surveying and most Earth science disciplines (e.g. exploration geophysics, hydrology, ecology, meteorology, oceanography, glaciology, geology). It also has military, intelligence, commercial, economic, planning, and humanitarian applications, among others.

In current usage, the term remote sensing generally refers to the use of satellite- or airborne-based sensor technologies to detect and classify objects on Earth. It includes the surface and the atmosphere and oceans, based on propagated signals (e.g. electromagnetic radiation). It may be split into "active" remote sensing (when a signal is emitted by a sensor mounted on a satellite or aircraft to the object and its reflection is detected by the sensor) and "passive" remote sensing (when the reflection of sunlight is detected by the sensor).

## Overview

Remote sensing can be divided into two types of methods: Passive remote sensing and active remote sensing. Passive sensors gather radiation that is emitted or reflected by the object or surrounding areas. Reflected sunlight is the most common source of radiation measured by passive sensors. Examples of passive remote sensors include film photography, infrared, charge-coupled devices, and radiometers. Active collection, on the other hand, emits energy in order to scan objects and areas whereupon a sensor then detects and measures the radiation that is reflected or backscattered from the target. RADAR and LiDAR are examples of active remote sensing where the time delay between emission and return is measured, establishing the location, speed and direction of an object.

Remote sensing makes it possible to collect data of dangerous or inaccessible areas. Remote sensing applications include monitoring deforestation in areas such as the Amazon Basin, glacial features in Arctic and Antarctic regions, and depth sounding of coastal and ocean depths. Military collection during the Cold War made use of stand-off collection of data about dangerous border areas. Remote sensing also replaces costly and slow data collection on the ground, ensuring in the process that areas or objects are not disturbed.

Orbital platforms collect and transmit data from different parts of the electromagnetic spectrum, which in conjunction with larger scale aerial or ground-based sensing and analysis, provides researchers with enough information to monitor trends such as El Niño and other natural long and short term phenomena. Other uses include different areas of the earth sciences such as natural resource management, agricultural fields such as land usage and conservation, greenhouse gas monitoring, oil spill detection and monitoring, and national security and overhead, ground-based and stand-off collection on border areas.

## Data quality

The quality of remote sensing data consists of its spatial, spectral, radiometric and temporal resolutions.

Spatial resolution
The size of a pixel that is recorded in a raster image - typically pixels may correspond to square areas ranging in side length from 1 to 1,000 metres (3.3 to 3,280.8 ft).

Spectral resolution
The bandwidth of the different frequency bands recorded - usually, this is related to the number of frequency bands recorded by the platform. Current Landsat collection is that of seven bands, including several in the infrared spectrum, ranging from a spectral resolution of 0.7 to 2.1 μm. The Hyperion sensor on Earth Observing-1 resolves 220 bands from 0.4 to 2.5 μm, with a spectral resolution of 0.10 to 0.11 μm per band.

Radiometric resolution
The number of different intensities of radiation the sensor is able to distinguish. Typically, this ranges from 8 to 14 bits, corresponding to 256 levels of the gray scale and up to 16,384 intensities or "shades" of colour, in each band. It also depends on the instrument noise.

Temporal resolution
The frequency of flyovers by the satellite or plane, and is only relevant in time-series studies or those requiring an averaged or mosaic image as in deforesting monitoring. This was first used by the intelligence community where repeated coverage revealed changes in infrastructure, the deployment of units or the modification/introduction of equipment. Cloud cover over a given area or object makes it necessary to repeat the collection of said location.

## Data processing

In order to create sensor-based maps, most remote sensing systems expect to extrapolate sensor data in relation to a reference point including distances between known points on the ground. This depends on the type of sensor used. For example, in conventional photographs, distances are accurate in the center of the image, with the distortion of measurements increasing the farther you get from the center. Another factor is that of the platen against which the film is pressed can cause severe errors when photographs are used to measure ground distances. The step in which this problem is resolved is called georeferencing and involves computer-aided matching of points in the image (typically 30 or more points per image) which is extrapolated with the use of an established benchmark, "warping" the image to produce accurate spatial data. As of the early 1990s, most satellite images are sold fully georeferenced.

In addition, images may need to be radiometrically and atmospherically corrected.

Radiometric correction
Allows avoidance of radiometric errors and distortions. The illumination of objects on the Earth's surface is uneven because of different properties of the relief. This factor is taken into account in the method of radiometric distortion correction. Radiometric correction gives a scale to the pixel values, e. g. the monochromatic scale of 0 to 255 will be converted to actual radiance values.

Topographic correction (also called terrain correction)
In rugged mountains, as a result of terrain, the effective illumination of pixels varies considerably. In a remote sensing image, the pixel on the shady slope receives weak illumination and has a low radiance value, in contrast, the pixel on the sunny slope receives strong illumination and has a high radiance value. For the same object, the pixel radiance value on the shady slope will be different from that on the sunny slope. Additionally, different objects may have similar radiance values. These ambiguities seriously affected remote sensing image information extraction accuracy in mountainous areas. It became the main obstacle to the further application of remote sensing images. The purpose of topographic correction is to eliminate this effect, recovering the true reflectivity or radiance of objects in horizontal conditions. It is the premise of quantitative remote sensing application.

Atmospheric correction
Elimination of atmospheric haze by rescaling each frequency band so that its minimum value (usually realised in water bodies) corresponds to a pixel value of 0. The digitizing of data also makes it possible to manipulate the data by changing gray-scale values.

## Data processing levels

To facilitate the discussion of data processing in practice, several processing "levels" were first defined in 1986 by NASA as part of its Earth Observing System and steadily adopted since then:

Level 0: Reconstructed, unprocessed instrument and payload data at full resolution, with any and all communications artifacts (e. g., synchronization frames, communications headers, duplicate data) removed.

Level 1a: Reconstructed, unprocessed instrument data at full resolution, time-referenced, and annotated with ancillary information, including radiometric and geometric calibration coefficients and georeferencing parameters (e. g., platform ephemeris) computed and appended but not applied to the Level 0 data (or if applied, in a manner that level 0 is fully recoverable from level 1a data).

Level 1b: Level 1a data that have been processed to sensor units (e. g., radar backscatter cross section, brightness temperature, etc.); not all instruments have Level 1b data; level 0 data is not recoverable from level 1b data.

Level 2: Derived geophysical variables (e. g., ocean wave height, soil moisture, ice concentration) at the same resolution and location as Level 1 source data.

Level 3: Variables mapped on uniform spacetime grid scales, usually with some completeness and consistency (e. g., missing points interpolated, complete regions mosaicked together from multiple orbits, etc.).

Level 4: Model output or results from analyses of lower level data (i. e., variables that were not measured by the instruments but instead are derived from these measurements).

A Level 1 data record is the most fundamental (i. e., highest reversible level) data record that has significant scientific utility, and is the foundation upon which all subsequent data sets are produced. Level 2 is the first level that is directly usable for most scientific applications; its value is much greater than the lower levels. Level 2 data sets tend to be less voluminous than Level 1 data because they have been reduced temporally, spatially, or spectrally. Level 3 data sets are generally smaller than lower level data sets and thus can be dealt with without incurring a great deal of data handling overhead. These data tend to be generally more useful for many applications. The regular spatial and temporal organization of Level 3 datasets makes it feasible to readily combine data from different sources.

---

# Source: https://crisp.nus.edu.sg/~research/tutorial/image.htm

## Digital Image Fundamentals

"A digital image is a two-dimensional array of pixels. Each pixel has an intensity value (represented by a digital number) and a location address (referenced by its row and column numbers)."

### Pixels

A digital image comprises of a two dimensional array of individual picture elements called pixels arranged in columns and rows. Each pixel represents an area on the Earth's surface. A pixel has an intensity value and a location address in the two dimensional image.

The intensity value represents the measured physical quantity such as the solar radiance in a given wavelength band reflected from the ground, emitted infrared radiation or backscattered radar intensity. This value is normally the average value for the whole ground area covered by the pixel.

The intensity of a pixel is digitised and recorded as a digital number. Due to the finite storage capacity, a digital number is stored with a finite number of bits (binary digits). The number of bits determine the radiometric resolution of the image. For example, an 8-bit digital number ranges from 0 to 255 (i.e. 2⁸ - 1), while a 11-bit digital number ranges from 0 to 2047. The detected intensity value needs to be scaled and quantized to fit within this range of value. In a Radiometrically Calibrated image, the actual intensity value can be derived from the pixel digital number.

The address of a pixel is denoted by its row and column coordinates in the two-dimensional image. There is a one-to-one correspondence between the column-row address of a pixel and the geographical coordinates (e.g. Longitude, latitude) of the imaged location.

### Multispectral Image

A multispectral image consists of a few image layers, each layer represents an image acquired at a particular wavelength band. For example, the SPOT HRV sensor operating in the multispectral mode detects radiations in three wavelength bands: the green (500 - 590 nm), red (610 - 680 nm) and near infrared (790 - 890 nm) bands. A single SPOT multispectral scene consists of three intensity images in the three wavelength bands. In this case, each pixel of the scene has three intensity values corresponding to the three bands. A multispectral IKONOS image consists of four bands: Blue, Green, Red and Near Infrared, while a landsat TM multispectral image consists of seven bands: blue, green, red, near-IR bands, two SWIR bands, and a thermal IR band.

### Superspectral Image

The more recent satellite sensors are capable of acquiring images at many more wavelength bands. For example, the MODIS sensor on-board the NASA's TERRA satellite consists of 36 spectral bands, covering the wavelength regions ranging from the visible, near infrared, short-wave infrared to the thermal infrared. The bands have narrower bandwidths, enabling the finer spectral characteristics of the targets to be captured by the sensor. The term "superspectral" has been coined to describe such sensors.

### Hyperspectral Image

A hyperspectral image consists of about a hundred or more contiguous spectral bands. The characteristic spectrum of the target pixel is acquired in a hyperspectral image. The precise spectral information contained in a hyperspectral image enables better characterisation and identification of targets. Hyperspectral images have potential applications in such fields as precision agriculture (e.g. monitoring the types, health, moisture status and maturity of crops), coastal management (e.g. monitoring of phytoplanktons, pollution, bathymetry changes).
Currently, hyperspectral imagery is not commercially available from satellites. There are experimental satellite-sensors that acquire hyperspectral imagery for scientific investigation (e.g. NASA's Hyperion sensor on-board the EO1 satellite, CHRIS sensor onboard ESA's PRABO satellite).

### Spatial Resolution

Spatial resolution refers to the size of the smallest object that can be resolved on the ground. In a digital image, the resolution is limited by the pixel size, i.e. the smallest resolvable object cannot be smaller than the pixel size. The intrinsic resolution of an imaging system is determined primarily by the instantaneous field of view (IFOV) of the sensor, which is a measure of the ground area viewed by a single detector element in a given instant in time. However this intrinsic resolution can often be degraded by other factors which introduce blurring of the image, such as improper focusing, atmospheric scattering and target motion.
