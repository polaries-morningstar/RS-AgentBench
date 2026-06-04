# RGB & Spectral Vegetation Indices

Source: https://awesome-ee-spectral-indices.readthedocs.io/en/latest/list.html
Source: https://www.indexdatabase.de/db/i.php
Source: https://plantsciencedronemethods.github.io/pages/VegetationIndices/Methods.html

Spectral Indices by Type

Note

All spectral indices listed here are considered broad-band spectral indices. Narrow-band spectral indices are coerced to the closest broad-band spectrum.

Vegetation
Vegetation Spectral Indices

Index

	

Long Name

	

Equation




AFRI1600

	

Aerosol Free Vegetation Index (1600 nm) [ref]

	

(N -0.66 *S1)/(N +0.66 *S1)




AFRI2100

	

Aerosol Free Vegetation Index (2100 nm) [ref]

	

(N -0.5 *S2)/(N +0.5 *S2)




ARI

	

Anthocyanin Reflectance Index [ref]

	

(1/G) -(1/RE1)




ARI2

	

Anthocyanin Reflectance Index 2 [ref]

	

N *((1/G) -(1/RE1))




ARVI

	

Atmospherically Resistant Vegetation Index [ref]

	

(N -(R -γ *(R -B)))/(N +(R -γ *(R -B)))




ATSAVI

	

Adjusted Transformed Soil-Adjusted Vegetation Index [ref]

	

sla *(N -sla *R -slb)/(sla *N +R -sla *slb +0.08 *(1 +sla2.0))




AVI

	

Advanced Vegetation Index [ref]

	

(N*(1.0-R)*(N-R))(1/3)




BCC

	

Blue Chromatic Coordinate [ref]

	

B/(R +G +B)




BNDVI

	

Blue Normalized Difference Vegetation Index [ref]

	

(N -B)/(N +B)




BWDRVI

	

Blue Wide Dynamic Range Vegetation Index [ref]

	

(α *N -B)/(α *N +B)




CCI

	

Chlorophyll Carotenoid Index [ref]

	

(G1 -R)/(G1 +R)




CIG

	

Chlorophyll Index Green [ref]

	

(N/G) -1.0




CIRE

	

Chlorophyll Index Red Edge [ref]

	

(N/RE1) -1




CRI550

	

Carotenoid Reflectance Index using 550 nm [ref]

	

(1.0/B) -(1.0/G)




CRI700

	

Carotenoid Reflectance Index using 700 nm [ref]

	

(1.0/B) -(1.0/RE1)




CRSWIR

	

Continuum Removal SWIR [ref]

	

S1/(N2 +((S2 -N2)/(lambdaS2 -λN2)) *(lambdaS1 -λN2))




CVI

	

Chlorophyll Vegetation Index [ref]

	

(N *R)/(G2.0)




DSI

	

Drought Stress Index [ref]

	

S1/N




DSWI1

	

Disease-Water Stress Index 1 [ref]

	

N/S1




DSWI2

	

Disease-Water Stress Index 2 [ref]

	

S1/G




DSWI3

	

Disease-Water Stress Index 3 [ref]

	

S1/R




DSWI4

	

Disease-Water Stress Index 4 [ref]

	

G/R




DSWI5

	

Disease-Water Stress Index 5 [ref]

	

(N +G)/(S1 +R)




DVI

	

Difference Vegetation Index [ref]

	

N -R




DVIplus

	

Difference Vegetation Index Plus [ref]

	

((λN -λR)/(λN -λG)) *G +(1.0 -((λN -λR)/(λN -λG))) *N -R




EBI

	

Enhanced Bloom Index [ref]

	

(R +G +B)/((G/B) *(R -B +epsilon))




ENDVI

	

Enhanced Normalized Difference Vegetation Index [ref]

	

((N +G) -(2 *B))/((N +G) +(2 *B))




EVI

	

Enhanced Vegetation Index [ref]

	

g *(N -R)/(N +C1 *R -C2 *B +L)




EVI2

	

Two-Band Enhanced Vegetation Index [ref]

	

g *(N -R)/(N +2.4 *R +L)




EVIv

	

Enhanced Vegetation Index of Vegetation [ref]

	

2.5 *((N -R)/(N +6 *R -7.5 *B +1.0)) *N




ExG

	

Excess Green Index [ref]

	

2 *G -R -B




ExGR

	

ExG - ExR Vegetation Index [ref]

	

(2.0 *G -R -B) -(1.3 *R -G)




ExR

	

Excess Red Index [ref]

	

1.3 *R -G




FCVI

	

Fluorescence Correction Vegetation Index [ref]

	

N -((R +G +B)/3.0)




GARI

	

Green Atmospherically Resistant Vegetation Index [ref]

	

(N -(G -(B -R)))/(N -(G +(B -R)))




GBNDVI

	

Green-Blue Normalized Difference Vegetation Index [ref]

	

(N -(G +B))/(N +(G +B))




GCC

	

Green Chromatic Coordinate [ref]

	

G/(R +G +B)




GDVI

	

Generalized Difference Vegetation Index [ref]

	

((Nn) -(Rn))/((Nn) +(Rn))




GEMI

	

Global Environment Monitoring Index [ref]

	

((2.0 *((N2.0) -(R2.0)) +1.5 *N +0.5 *R)/(N +R +0.5)) *(1.0 -0.25 *((2.0 *((N2.0) -(R2)) +1.5 *N +0.5 *R)/(N +R +0.5))) -((R -0.125)/(1 -R))




GLI

	

Green Leaf Index [ref]

	

(2.0 *G -R -B)/(2.0 *G +R +B)




GM1

	

Gitelson and Merzlyak Index 1 [ref]

	

RE2/G




GM2

	

Gitelson and Merzlyak Index 2 [ref]

	

RE2/RE1




GNDVI

	

Green Normalized Difference Vegetation Index [ref]

	

(N -G)/(N +G)




GOSAVI

	

Green Optimized Soil Adjusted Vegetation Index [ref]

	

(N -G)/(N +G +0.16)




GRNDVI

	

Green-Red Normalized Difference Vegetation Index [ref]

	

(N -(G +R))/(N +(G +R))




GRVI

	

Green Ratio Vegetation Index [ref]

	

N/G




GSAVI

	

Green Soil Adjusted Vegetation Index [ref]

	

(1.0 +L) *(N -G)/(N +G +L)




GVMI

	

Global Vegetation Moisture Index [ref]

	

((N +0.1) -(S2 +0.02))/((N +0.1) +(S2 +0.02))




IAVI

	

New Atmospherically Resistant Vegetation Index [ref]

	

(N -(R -γ *(B -R)))/(N +(R -γ *(B -R)))




IKAW

	

Kawashima Index [ref]

	

(R -B)/(R +B)




IPVI

	

Infrared Percentage Vegetation Index [ref]

	

N/(N +R)




IRECI

	

Inverted Red-Edge Chlorophyll Index [ref]

	

(RE3 -R)/(RE1/RE2)




IRGBVI

	

Improved-Red-Green-Blue Vegetation Index [ref]

	

(5.0 *(G2.0) -2.0 *(R2.0) -5.0 *(B2.0))/(5.0 *(G2.0) +2.0 *(R2.0) +5.0 *(B2.0))




MCARI

	

Modified Chlorophyll Absorption in Reflectance Index [ref]

	

((RE1 -R) -0.2 *(RE1 -G)) *(RE1/R)




MCARI1

	

Modified Chlorophyll Absorption in Reflectance Index 1 [ref]

	

1.2 *(2.5 *(N -R) -1.3 *(N -G))




MCARI2

	

Modified Chlorophyll Absorption in Reflectance Index 2 [ref]

	

(1.5 *(2.5 *(N -R) -1.3 *(N -G)))/((((2.0*N+1)2)-(6.0*N-5*(R0.5))-0.5)0.5)




MCARI705

	

Modified Chlorophyll Absorption in Reflectance Index (705 and 750 nm) [ref]

	

((RE2 -RE1) -0.2 *(RE2 -G)) *(RE2/RE1)




MCARIOSAVI

	

MCARI/OSAVI Ratio [ref]

	

(((RE1 -R) -0.2 *(RE1 -G)) *(RE1/R))/(1.16 *(N -R)/(N +R +0.16))




MCARIOSAVI705

	

MCARI/OSAVI Ratio (705 and 750 nm) [ref]

	

(((RE2 -RE1) -0.2 *(RE2 -G)) *(RE2/RE1))/(1.16 *(RE2 -RE1)/(RE2 +RE1 +0.16))




MGRVI

	

Modified Green Red Vegetation Index [ref]

	

(G2.0 -R2.0)/(G2.0 +R2.0)




MI

	

Mangrove Index [ref]

	

(N -S1)/(N *S1)




MNDVI

	

Modified Normalized Difference Vegetation Index [ref]

	

(N -S2)/(N +S2)




MNLI

	

Modified Non-Linear Vegetation Index [ref]

	

(1 +L) *((N2) -R)/((N2) +R +L)




MRBVI

	

Modified Red Blue Vegetation Index [ref]

	

(R2.0 -B2.0)/(R2.0 +B2.0)




MSAVI

	

Modified Soil-Adjusted Vegetation Index [ref]

	

0.5 *(2.0 *N +1 -(((2*N+1)2)-8*(N-R))0.5)




MSI

	

Moisture Stress Index [ref]

	

S1/N




MSR

	

Modified Simple Ratio [ref]

	

(N/R -1)/((N/R+1)0.5)




MSR705

	

Modified Simple Ratio (705 and 750 nm) [ref]

	

(RE2/RE1 -1)/((RE2/RE1+1)0.5)




MTCI

	

MERIS Terrestrial Chlorophyll Index [ref]

	

(RE2 -RE1)/(RE1 -R)




MTVI1

	

Modified Triangular Vegetation Index 1 [ref]

	

1.2 *(1.2 *(N -G) -2.5 *(R -G))




MTVI2

	

Modified Triangular Vegetation Index 2 [ref]

	

(1.5 *(1.2 *(N -G) -2.5 *(R -G)))/((((2.0*N+1)2)-(6.0*N-5*(R0.5))-0.5)0.5)




MVI

	

Mangrove Vegetation Index [ref]

	

(N -G)/(S1 -G)




ND705

	

Normalized Difference (705 and 750 nm) [ref]

	

(RE2 -RE1)/(RE2 +RE1)




NDDI

	

Normalized Difference Drought Index [ref]

	

(((N -R)/(N +R)) -((G -N)/(G +N)))/(((N -R)/(N +R)) +((G -N)/(G +N)))




NDGI

	

Normalized Difference Greenness Index [ref]

	

(((λN -λR)/(λN -λG)) *G +(1.0 -((λN -λR)/(λN -λG))) *N -R)/(((λN -λR)/(λN -λG)) *G +(1.0 -((λN -λR)/(λN -λG))) *N +R)




NDII

	

Normalized Difference Infrared Index [ref]

	

(N -S1)/(N +S1)




NDMI

	

Normalized Difference Moisture Index [ref]

	

(N -S1)/(N +S1)




NDPI

	

Normalized Difference Phenology Index [ref]

	

(N -(α *R +(1.0 -α) *S1))/(N +(α *R +(1.0 -α) *S1))




NDREI

	

Normalized Difference Red Edge Index [ref]

	

(N -RE1)/(N +RE1)




NDTI4RE

	

4-band Red Edge Normalized Difference Tillage Index [ref]

	

γ *(S1 -S2)/(S1 +S2) +(1 -γ) *(N -RE3)/(N +RE3)




NDTillI

	

Normalized Difference Tillage Index [ref]

	

(S1 -S2)/(S1 +S2)




NDVI

	

Normalized Difference Vegetation Index [ref]

	

(N -R)/(N +R)




NDVI4RE

	

4-band Red Edge Normalized Difference Vegetation Index [ref]

	

((α *RE3 +(1 -α) *RE2) -(β *R +(1 -β) *RE1))/((α *RE3 +(1 -α) *RE2) +(β *R +(1 -β) *RE1))




NDVI705

	

Normalized Difference Vegetation Index (705 and 750 nm) [ref]

	

(RE2 -RE1)/(RE2 +RE1)




NDYI

	

Normalized Difference Yellowness Index [ref]

	

(G -B)/(G +B)




NGRDI

	

Normalized Green Red Difference Index [ref]

	

(G -R)/(G +R)




NIRv

	

Near-Infrared Reflectance of Vegetation [ref]

	

((N -R)/(N +R)) *N




NIRvH2

	

Hyperspectral Near-Infrared Reflectance of Vegetation [ref]

	

N -R -k *(λN -λR)




NIRvP

	

Near-Infrared Reflectance of Vegetation and Incoming PAR [ref]

	

((N -R)/(N +R)) *N *PAR




NLI

	

Non-Linear Vegetation Index [ref]

	

((N2) -R)/((N2) +R)




NMDI

	

Normalized Multi-band Drought Index [ref]

	

(N -(S1 -S2))/(N +(S1 -S2))




NPCI

	

Normalized Pigments Chlorophyll Ratio Index [ref]

	

(R -A)/(R +A)




NRFIg

	

Normalized Rapeseed Flowering Index Green [ref]

	

(G -S2)/(G +S2)




NRFIr

	

Normalized Rapeseed Flowering Index Red [ref]

	

(R -S2)/(R +S2)




NormG

	

Normalized Green [ref]

	

G/(N +G +R)




NormNIR

	

Normalized NIR [ref]

	

N/(N +G +R)




NormR

	

Normalized Red [ref]

	

R/(N +G +R)




OCVI

	

Optimized Chlorophyll Vegetation Index [ref]

	

(N/G) *(R/G)c




OSAVI

	

Optimized Soil-Adjusted Vegetation Index [ref]

	

(N -R)/(N +R +0.16)




PSRI

	

Plant Senescing Reflectance Index [ref]

	

(R -B)/RE2




RCC

	

Red Chromatic Coordinate [ref]

	

R/(R +G +B)




RDVI

	

Renormalized Difference Vegetation Index [ref]

	

(N -R)/((N+R)0.5)




REDSI

	

Red-Edge Disease Stress Index [ref]

	

((705.0 -665.0) *(RE3 -R) -(783.0 -665.0) *(RE1 -R))/(2.0 *R)




RENDVI

	

Red Edge Normalized Difference Vegetation Index [ref]

	

(RE2 -RE1)/(RE2 +RE1)




RGBVI

	

Red Green Blue Vegetation Index [ref]

	

(G2.0 -B *R)/(G2.0 +B *R)




RGRI

	

Red-Green Ratio Index [ref]

	

R/G




RI

	

Redness Index [ref]

	

(R -G)/(R +G)




RVI

	

Ratio Vegetation Index [ref]

	

RE2/R




RVI4RE

	

4-band Red Edge Ratio Vegetation Index [ref]

	

(α *RE3 +(1 -α) *RE2)/(β *R +(1 -β) *RE1)




S2REP

	

Sentinel-2 Red-Edge Position [ref]

	

705.0 +35.0 *((((RE3 +R)/2.0) -RE1)/(RE2 -RE1))




SARVI

	

Soil Adjusted and Atmospherically Resistant Vegetation Index [ref]

	

(1 +L) *(N -(R -(R -B)))/(N +(R -(R -B)) +L)




SAVI

	

Soil-Adjusted Vegetation Index [ref]

	

(1.0 +L) *(N -R)/(N +R +L)




SAVI2

	

Soil-Adjusted Vegetation Index 2 [ref]

	

N/(R +(slb/sla))




SAVI4RE

	

4-band Red Edge Soil Adjusted Vegetation Index [ref]

	

2.0 *((α *RE3 +(1 -α) *RE2) -(β *R +(1 -β) *RE1))/((α *RE3 +(1 -α) *RE2) +(β *R +(1 -β) *RE1 +1))




SEVI

	

Shadow-Eliminated Vegetation Index [ref]

	

(N/R) +fdelta *(1.0/R)




SI

	

Shadow Index [ref]

	

((1.0-B)*(1.0-G)*(1.0-R))(1/3)




SIPI

	

Structure Insensitive Pigment Index [ref]

	

(N -A)/(N -R)




SLAVI

	

Specific Leaf Area Vegetation Index [ref]

	

N/(R +S2)




SNDTI

	

Soil-Adjusted Normalized Difference Tillage Index [ref]

	

(1.0 +L) *(S1 -S2)/(S1 +S2 +L)




SNDTI4RE

	

4-band Red Edge Soil-Adjusted Normalized Difference Tillage Index [ref]

	

γ *((S1 -S2) *2.0)/(S1 +S2 +1.0) +(1 -γ) *((N -RE3) *2.0)/(N +RE3 +1.0)




SR

	

Simple Ratio [ref]

	

N/R




SR2

	

Simple Ratio (800 and 550 nm) [ref]

	

N/G




SR3

	

Simple Ratio (860, 550 and 708 nm) [ref]

	

N2/(G *RE1)




SR555

	

Simple Ratio (555 and 750 nm) [ref]

	

RE2/G




SR705

	

Simple Ratio (705 and 750 nm) [ref]

	

RE2/RE1




STI

	

Simple Tillage Index [ref]

	

S1/S2




STI4RE

	

4-band Red Edge Soil Tillage Index [ref]

	

γ *S1/S2 +(1 -γ) *N/RE3




SeLI

	

Sentinel-2 LAI Green Index [ref]

	

(N2 -RE1)/(N2 +RE1)




TCARI

	

Transformed Chlorophyll Absorption in Reflectance Index [ref]

	

3 *((RE1 -R) -0.2 *(RE1 -G) *(RE1/R))




TCARIOSAVI

	

TCARI/OSAVI Ratio [ref]

	

(3 *((RE1 -R) -0.2 *(RE1 -G) *(RE1/R)))/(1.16 *(N -R)/(N +R +0.16))




TCARIOSAVI705

	

TCARI/OSAVI Ratio (705 and 750 nm) [ref]

	

(3 *((RE2 -RE1) -0.2 *(RE2 -G) *(RE2/RE1)))/(1.16 *(RE2 -RE1)/(RE2 +RE1 +0.16))




TCI

	

Triangular Chlorophyll Index [ref]

	

1.2 *(RE1 -G) -1.5 *(R -G) *(RE1/R)0.5




TDVI

	

Transformed Difference Vegetation Index [ref]

	

1.5 *((N -R)/((N2.0+R+0.5)0.5))




TGI

	

Triangular Greenness Index [ref]

	

-0.5 *(190 *(R -G) -120 *(R -B))




TRRVI

	

Transformed Red Range Vegetation Index [ref]

	

((RE2 -R)/(RE2 +R))/(((N -R)/(N +R)) +1.0)




TSAVI

	

Transformed Soil-Adjusted Vegetation Index [ref]

	

sla *(N -sla *R -slb)/(sla *N +R -sla *slb)




TTVI

	

Transformed Triangular Vegetation Index [ref]

	

0.5 *((865.0 -740.0) *(RE3 -RE2) -(N2 -RE2) *(783.0 -740))




TVI

	

Transformed Vegetation Index [ref]

	

(((N-R)/(N+R))+0.5)0.5




TriVI

	

Triangular Vegetation Index [ref]

	

0.5 *(120 *(N -G) -200 *(R -G))




VARI

	

Visible Atmospherically Resistant Index [ref]

	

(G -R)/(G +R -B)




VARI700

	

Visible Atmospherically Resistant Index (700 nm) [ref]

	

(RE1 -1.7 *R +0.7 *B)/(RE1 +1.3 *R -1.3 *B)




VI700

	

Vegetation Index (700 nm) [ref]

	

(RE1 -R)/(RE1 +R)




VIG

	

Vegetation Index Green [ref]

	

(G -R)/(G +R)




WDRVI

	

Wide Dynamic Range Vegetation Index [ref]

	

(α *N -R)/(α *N +R)




WDVI

	

Weighted Difference Vegetation Index [ref]

	

N -sla *R




bNIRv

	

Blue Near-Infrared Reflectance of Vegetation [ref]

	

((N -B)/(N +B)) *N




mND705

	

Modified Normalized Difference (705, 750 and 445 nm) [ref]

	

(RE2 -RE1)/(RE2 +RE1 -A)




mSR705

	

Modified Simple Ratio (705 and 445 nm) [ref]

	

(RE2 -A)/(RE2 +A)




sNIRvLSWI

	

SWIR-enhanced Near-Infrared Reflectance of Vegetation for LSWI [ref]

	

((N -S2)/(N +S2)) *N




sNIRvNDPI

	

SWIR-enhanced Near-Infrared Reflectance of Vegetation for NDPI [ref]

	

(N -(α *R +(1.0 -α) *S2))/(N +(α *R +(1.0 -α) *S2)) *N




sNIRvNDVILSWIP

	

SWIR-enhanced Near-Infrared Reflectance of Vegetation for the NDVI-LSWI Product [ref]

	

((N -R)/(N +R)) *((N -S2)/(N +S2)) *N




sNIRvNDVILSWIS

	

SWIR-enhanced Near-Infrared Reflectance of Vegetation for the NDVI-LSWI Sum [ref]

	

(((N -R)/(N +R)) +((N -S2)/(N +S2))) *N




sNIRvSWIR

	

SWIR-enhanced Near-Infrared Reflectance of Vegetation [ref]

	

((N -R -S22.0)/(N +R +S22.0)) *N

Burn
Burn Spectral Indices

Index

	

Long Name

	

Equation




BAI

	

Burned Area Index [ref]

	

1.0/((0.1-R)2.0 +(0.06-N)2.0)




BAIM

	

Burned Area Index adapted to MODIS [ref]

	

1.0/((0.05-N)2.0) +((0.2-S2)2.0)




BAIS2

	

Burned Area Index for Sentinel 2 [ref]

	

(1.0 -((RE2*RE3*N2)/R)0.5) *(((S2 -N2)/(S2+N2)0.5) +1.0)




CSI

	

Char Soil Index [ref]

	

N/S2




CSIT

	

Char Soil Index Thermal [ref]

	

N/(S2 *T/10000.0)




MIRBI

	

Mid-Infrared Burn Index [ref]

	

10.0 *S2 -9.8 *S1 +2.0




NBR

	

Normalized Burn Ratio [ref]

	

(N -S2)/(N +S2)




NBR2

	

Normalized Burn Ratio 2 [ref]

	

(S1 -S2)/(S1 +S2)




NBRSWIR

	

Normalized Burn Ratio SWIR [ref]

	

(S2 -S1 -0.02)/(S2 +S1 +0.1)




NBRT1

	

Normalized Burn Ratio Thermal 1 [ref]

	

(N -(S2 *T/10000.0))/(N +(S2 *T/10000.0))




NBRT2

	

Normalized Burn Ratio Thermal 2 [ref]

	

((N/(T/10000.0)) -S2)/((N/(T/10000.0)) +S2)




NBRT3

	

Normalized Burn Ratio Thermal 3 [ref]

	

((N -(T/10000.0)) -S2)/((N -(T/10000.0)) +S2)




NBRplus

	

Normalized Burn Ratio Plus [ref]

	

(S2 -N2 -G -B)/(S2 +N2 +G +B)




NDSWIR

	

Normalized Difference SWIR [ref]

	

(N -S1)/(N +S1)




NDVIT

	

Normalized Difference Vegetation Index Thermal [ref]

	

(N -(R *T/10000.0))/(N +(R *T/10000.0))




NSTv1

	

NIR-SWIR-Temperature Version 1 [ref]

	

((N -S2)/(N +S2)) *T




NSTv2

	

NIR-SWIR-Temperature Version 2 [ref]

	

(N -(S2 +T))/(N +(S2 +T))




SAVIT

	

Soil-Adjusted Vegetation Index Thermal [ref]

	

(1.0 +L) *(N -(R *T/10000.0))/(N +(R *T/10000.0) +L)




VI6T

	

VI6T Index [ref]

	

(N -T/10000.0)/(N +T/10000.0)

Water
Water Spectral Indices

Index

	

Long Name

	

Equation




ANDWI

	

Augmented Normalized Difference Water Index [ref]

	

(B +G +R -N -S1 -S2)/(B +G +R +N +S1 +S2)




AWEInsh

	

Automated Water Extraction Index [ref]

	

4.0 *(G -S1) -0.25 *N +2.75 *S2




AWEIsh

	

Automated Water Extraction Index with Shadows Elimination [ref]

	

B +2.5 *G -1.5 *(N +S1) -0.25 *S2




FAI

	

Floating Algae Index [ref]

	

N -(R +(S1 -R) *((λN -λR)/(lambdaS1 -λR)))




FDI

	

Floating Debris Index [ref]

	

N -(RE2 +10 *(S1 -RE2) *(λN -λR)/(lambdaS1 -λR))




FWEI

	

Flood/Water Extraction Index [ref]

	

(((B +G +R)/3.0) -N)/(((B +G +R)/3.0) +N)




LSWI

	

Land Surface Water Index [ref]

	

(N -S1)/(N +S1)




MBWI

	

Multi-Band Water Index [ref]

	

(ω *G) -R -N -S1 -S2




MLSWI26

	

Modified Land Surface Water Index (MODIS Bands 2 and 6) [ref]

	

(1.0 -N -S1)/(1.0 -N +S1)




MLSWI27

	

Modified Land Surface Water Index (MODIS Bands 2 and 7) [ref]

	

(1.0 -N -S2)/(1.0 -N +S2)




MNDWI

	

Modified Normalized Difference Water Index [ref]

	

(G -S1)/(G +S1)




MuWIR

	

Revised Multi-Spectral Water Index [ref]

	

-4.0 *((B -G)/(B +G)) +2.0 *((G -N)/(G +N)) +2.0 *((G -S2)/(G +S2)) -((G -S1)/(G +S1))




NDCI

	

Normalized Difference Chlorophyll Index [ref]

	

(RE1 -R)/(RE1 +R)




NDPonI

	

Normalized Difference Pond Index [ref]

	

(S1 -G)/(S1 +G)




NDTI

	

Normalized Difference Turbidity Index [ref]

	

(R -G)/(R +G)




NDVIMNDWI

	

NDVI-MNDWI Model [ref]

	

((N -R)/(N +R)) -((G -S1)/(G +S1))




NDWI

	

Normalized Difference Water Index [ref]

	

(G -N)/(G +N)




NDWIns

	

Normalized Difference Water Index with no Snow Cover and Glaciers [ref]

	

(G -α *N)/(G +N)




NWI

	

New Water Index [ref]

	

(B -(N +S1 +S2))/(B +(N +S1 +S2))




OSI

	

Oil Spill Index [ref]

	

(G +R)/B




PI

	

Plastic Index [ref]

	

N/(N +R)




RNDVI

	

Reversed Normalized Difference Vegetation Index [ref]

	

(R -N)/(R +N)




RWI

	

Rescaled Water Index [ref]

	

((G(1.0/2.71828)) *(1.0/n) -S1)/((G(1.0/2.71828)) *(1.0/n) +S1)




S2WI

	

Sentinel-2 Water Index [ref]

	

(RE1 -S2)/(RE1 +S2)




SCoWI

	

Subtractive Coastal Water Index [ref]

	

B +2.0 *(G -N) -0.75 *S1 -0.5 *S2




SWM

	

Sentinel Water Mask [ref]

	

(B +G)/(N +S1)




TWI

	

Triangle Water Index [ref]

	

(2.84 *(RE1 -RE2)/(G +S2)) +((1.25 *(G -B) -(N -B))/(N +1.25 *G -0.25 *B))




WI1

	

Water Index 1 [ref]

	

(G -S2)/(G +S2)




WI2

	

Water Index 2 [ref]

	

(B -S2)/(B +S2)




WI2015

	

Water Index 2015 [ref]

	

1.7204 +171 *G +3 *R -70 *N -45 *S1 -71 *S2




WRI

	

Water Ratio Index [ref]

	

(G +R)/(N +S1)

Snow
Snow Spectral Indices

Index

	

Long Name

	

Equation




NBSIMS

	

Non-Binary Snow Index for Multi-Component Surfaces [ref]

	

0.36 *(G +R +N) -(((B +S2)/G) +S1)




NDGlaI

	

Normalized Difference Glacier Index [ref]

	

(G -R)/(G +R)




NDSI

	

Normalized Difference Snow Index [ref]

	

(G -S1)/(G +S1)




NDSII

	

Normalized Difference Snow Ice Index [ref]

	

(G -N)/(G +N)




NDSIITM

	

Normalized Difference Snow/Ice Index for Landsat TM [ref]

	

(R -S1)/(R +S1)




NDSInw

	

Normalized Difference Snow Index with no Water [ref]

	

(N -S1 -β)/(N +S1)




NDSaII

	

Normalized Difference Snow and Ice Index [ref]

	

(R -S1)/(R +S1)




S3

	

S3 Snow Index [ref]

	

(N *(R -S1))/((N +R) *(N +S1))




SWI

	

Snow Water Index [ref]

	

(G *(N -S1))/((G +N) *(N +S1))

Soil
Soil Spectral Indices

Index

	

Long Name

	

Equation




BI

	

Bare Soil Index [ref]

	

((S1 +R) -(N +B))/((S1 +R) +(N +B))




BITM

	

Landsat TM-based Brightness Index [ref]

	

(((B2.0)+(G2.0)+(R2.0))/3.0)0.5




BIXS

	

SPOT HRV XS-based Brightness Index [ref]

	

(((G2.0)+(R2.0))/2.0)0.5




BaI

	

Bareness Index [ref]

	

R +S1 -N




DBSI

	

Dry Bareness Index [ref]

	

((S1 -G)/(S1 +G)) -((N -R)/(N +R))




EMBI

	

Enhanced Modified Bare Soil Index [ref]

	

((((S1 -S2 -N)/(S1 +S2 +N)) +0.5) -((G -S1)/(G +S1)) -0.5)/((((S1 -S2 -N)/(S1 +S2 +N)) +0.5) +((G -S1)/(G +S1)) +1.5)




MBI

	

Modified Bare Soil Index [ref]

	

((S1 -S2 -N)/(S1 +S2 +N)) +0.5




NBLI

	

Normalized Difference Bare Land Index [ref]

	

(R -T)/(R +T)




NBLIOLI

	

Normalized Difference Bare Land Index for Landsat-OLI [ref]

	

(R -T1)/(R +T1)




NDBaI

	

Normalized Difference Bareness Index [ref]

	

(S1 -T)/(S1 +T)




NDSIWV

	

WorldView Normalized Difference Soil Index [ref]

	

(G -Y)/(G +Y)




NDSoI

	

Normalized Difference Soil Index [ref]

	

(S2 -G)/(S2 +G)




NSDS

	

Normalized Shortwave Infrared Difference Soil-Moisture [ref]

	

(S1 -S2)/(S1 +S2)




NSDSI1

	

Normalized Shortwave-Infrared Difference Bare Soil Moisture Index 1 [ref]

	

(S1 -S2)/S1




NSDSI2

	

Normalized Shortwave-Infrared Difference Bare Soil Moisture Index 2 [ref]

	

(S1 -S2)/S2




NSDSI3

	

Normalized Shortwave-Infrared Difference Bare Soil Moisture Index 3 [ref]

	

(S1 -S2)/(S1 +S2)




RI4XS

	

SPOT HRV XS-based Redness Index 4 [ref]

	

(R2.0)/(G4.0)

Urban
Urban Spectral Indices

Index

	

Long Name

	

Equation




BLFEI

	

Built-Up Land Features Extraction Index [ref]

	

(((G +R +S2)/3.0) -S1)/(((G +R +S2)/3.0) +S1)




BRBA

	

Band Ratio for Built-up Area [ref]

	

R/S1




DBI

	

Dry Built-Up Index [ref]

	

((B -T1)/(B +T1)) -((N -R)/(N +R))




EBBI

	

Enhanced Built-Up and Bareness Index [ref]

	

(S1 -N)/(10.0 *((S1+T)0.5))




IBI

	

Index-Based Built-Up Index [ref]

	

(((S1 -N)/(S1 +N)) -(((N -R) *(1.0 +L)/(N +R +L)) +((G -S1)/(G +S1)))/2.0)/(((S1 -N)/(S1 +N)) +(((N -R) *(1.0 +L)/(N +R +L)) +((G -S1)/(G +S1)))/2.0)




NBAI

	

Normalized Built-up Area Index [ref]

	

(S2 -S1/G)/(S2 +S1/G)




NBUI

	

New Built-Up Index [ref]

	

((S1 -N)/(10.0 *(T+S1)0.5)) -(((N -R) *(1.0 +L))/(N -R +L)) -(G -S1)/(G +S1)




NDBI

	

Normalized Difference Built-Up Index [ref]

	

(S1 -N)/(S1 +N)




NDISIb

	

Normalized Difference Impervious Surface Index Blue [ref]

	

(T -(B +N +S1)/3.0)/(T +(B +N +S1)/3.0)




NDISIg

	

Normalized Difference Impervious Surface Index Green [ref]

	

(T -(G +N +S1)/3.0)/(T +(G +N +S1)/3.0)




NDISImndwi

	

Normalized Difference Impervious Surface Index with MNDWI [ref]

	

(T -(((G -S1)/(G +S1)) +N +S1)/3.0)/(T +(((G -S1)/(G +S1)) +N +S1)/3.0)




NDISIndwi

	

Normalized Difference Impervious Surface Index with NDWI [ref]

	

(T -(((G -N)/(G +N)) +N +S1)/3.0)/(T +(((G -N)/(G +N)) +N +S1)/3.0)




NDISIr

	

Normalized Difference Impervious Surface Index Red [ref]

	

(T -(R +N +S1)/3.0)/(T +(R +N +S1)/3.0)




NHFD

	

Non-Homogeneous Feature Difference [ref]

	

(RE1 -A)/(RE1 +A)




PISI

	

Perpendicular Impervious Surface Index [ref]

	

0.8192 *B -0.5735 *N +0.0750




UI

	

Urban Index [ref]

	

(S2 -N)/(S2 +N)




VIBI

	

Vegetation Index Built-up Index [ref]

	

((N -R)/(N +R))/(((N -R)/(N +R)) +((S1 -N)/(S1 +N)))




VgNIRBI

	

Visible Green-Based Built-Up Index [ref]

	

(G -N)/(G +N)




VrNIRBI

	

Visible Red-Based Built-Up Index [ref]

	

(R -N)/(R +N)

Clouds
Clouds Spectral Indices

Index

	

Long Name

	

Equation




CI1SWIR

	

Cloud Index Form 1 with SWIR 1 [ref]

	

(N +2.0 *S1)/(B +G +R)




CI1woSWIR

	

Cloud Index Form 1 without SWIR bands [ref]

	

(3.0 *N)/(B +G +R)




CI2SWIR

	

Cloud Index Form 2 with SWIR bands [ref]

	

(B +G +R +N +S1 +S2)/6.0




CI2woSWIR

	

Cloud Index Form 2 without SWIR bands [ref]

	

(B +G +R +N)/4.0




CLOSDI

	

Cloud Shadow Detection Index [ref]

	

(1.0 -1.5 *N -0.1 *R)/(1.0 +3.5 *N +4.9 *R)




CSISWIR

	

Cloud Shadow Index with SWIR 1 [ref]

	

(N +S1)/2.0




CSIwoSWIR

	

Cloud Shadow Index without SWIR bands [ref]

	

N

Kernel

Warning

All kernel indices listed here were extracted from the Supplementary Material of Camps-Valls et al., 2021. Please note that the kEVI and kVARI indices may have more than one implementation, but for simplicity, just one is presented here.

Kernel Spectral Indices

Index

	

Long Name

	

Equation




kEVI

	

Kernel Enhanced Vegetation Index [ref]

	

g *(kNN -kNR)/(kNN +C1 *kNR -C2 *kNB +kNL)




kIPVI

	

Kernel Infrared Percentage Vegetation Index [ref]

	

kNN/(kNN +kNR)




kNDVI

	

Kernel Normalized Difference Vegetation Index [ref]

	

(kNN -kNR)/(kNN +kNR)




kRVI

	

Kernel Ratio Vegetation Index [ref]

	

kNN/kNR




kVARI

	

Kernel Visible Atmospherically Resistant Index [ref]

	

(kGG -kGR)/(kGG +kGR -kGB)

RADAR
RADAR Spectral Indices

Index

	

Long Name

	

Equation




DPDD

	

Dual-Pol Diagonal Distance [ref]

	

(VV +VH)/2.00.5




DpRVIHH

	

Dual-Polarized Radar Vegetation Index HH [ref]

	

(4.0 *HV)/(HH +HV)




DpRVIVV

	

Dual-Polarized Radar Vegetation Index VV [ref]

	

(4.0 *VH)/(VV +VH)




NDPolI

	

Normalized Difference Polarization Index [ref]

	

(VV -VH)/(VV +VH)




QpRVI

	

Quad-Polarized Radar Vegetation Index [ref]

	

(8.0 *HV)/(HH +VV +2.0 *HV)




RFDI

	

Radar Forest Degradation Index [ref]

	

(HH -HV)/(HH +HV)




VDDPI

	

Vertical Dual De-Polarization Index [ref]

	

(VV +VH)/VV




VHVVD

	

VH-VV Difference [ref]

	

VH -VV




VHVVP

	

VH-VV Product [ref]

	

VH *VV




VHVVR

	

VH-VV Ratio [ref]

	

VH/VV




VVVHD

	

VV-VH Difference [ref]

	

VV -VH




VVVHR

	

VV-VH Ratio [ref]

	

VV/VH




VVVHS

	

VV-VH Sum [ref]

	

VV +VH

Build and run apps in over 115 regions with MongoDB Atlas, the database for every enterprise.
Ads by EthicalAds
	
\"Previous\"
Awesome Spectral Indices
\"Next\"
Do you want to contribute?
© Copyright 2021, David Montero Loaiza.
Created using Sphinx 9.0.4. and Material for Sphinx"
"List of available Indices
Order by: Name [^][v] • Abbreviation [^][v] • Applications [^][v] • Sensors [^][v] • References [^][v]

Page 1 of 2 [1] [2] * > * >|

Nr	Name	Abbrev.	Formula	Variables	Source	# Sens.	# Appl.	# Ref.
1	Adjusted transformed soil-adjusted VI	ATSAVI	a
NIR-a*RED-b
a*NIR+RED-a*b+X(1+a2)
	X=0.08, a=1.22, b=0.03	Original Formula	87	2	3
2	Aerosol free vegetation index 1600	AFRI1600	(NIR-0.66
1600nm
NIR+0.661600nm
)
		Original Formula	37	3	2
3	Aerosol free vegetation index 2100	AFRI2100	(NIR-0.5
2100nm
NIR+0.562100nm
)
		Original Formula	19	3	2
4	Alteration		
[1600:1700]
[2145:2185]
		Derived	25	3	1
5	Alunite/Kaolinite/Pyrophylite		
[1600:1700]+[2185:2225]
[2145:2185]
		Derived	13	3	1
6	Amphibole		
[2185:2225]
[2295:2365]
		Derived	13	3	1
7	Amphibole / MgOH		
[2185:2225]+[2360:2430]
[2295:2365]
		Derived	12	2	1
8	Anthocyanin reflectance index	ARI	
1
550nm
-
1
700nm
		Original Formula	38	2	1
9	Ashburn Vegetation Index	AVI	2.0[800:1100]-[600:700]
		Original Formula	84	0	2
10	Atmospherically Resistant Vegetation Index	ARVI	
NIR-RED-y(RED-BLUE)
NIR+RED-y(RED-BLUE)
	NIR = [781:1399]	Original Formula	69	3	14
11	Atmospherically Resistant Vegetation Index 2	ARVI2	-0.18+1.17(
NIR-RED
NIR+RED
)
		Original Formula	87	3	1
12	Average reflectance 750 to 850	AR750/850	Averagereflectancebetween750nmand850nm
		Original Formula	28	1	2
13	Basic Degree Index - SIO2		
[8925:9275]
[10250:10950]
		Derived	5	3	2
14	Blue-wide dynamic range vegetation index	BWDRVI	
0.1NIR-BLUE
0.1NIR+BLUE
		Original Formula	71	1	1
15	Browning Reflectance Index	BRI	
1
550nm
-
1
700nm
NIR
		Original Formula	35	1	1
16	Canopy Chlorophyll Content Index	CCCI	
NIR-rededge
NIR+rededge
NIR-Red
NIR+Red
		Original Formula	69	4	5
17	Carbonate		
[10250:10950]
[10950:11650]
		Derived	6	2	2
18	Carbonate/Chlorite/Epidote		
[2235:2365]+[2360:2430]
[2295:2365]
		Derived	12	3	1
19	CASI NDVI	CASI NDVI	
([770:780]+[784:790])-([655:665]+[676:685])
([770:780]+[784:790])+([655:665]+[676:685])
		Original Formula	18	3	1
20	CASI TM4/3	CASI TM4/3	
[770:780]+[784:790]
[655:665]+[676:685]
		Original Formula	18	3	1
21	Cellulose Absorption Index	CAI	100(0.5(2030nm+2210nm)-2100nm)
		Original Formula	10	3	0
22	Cellulose absorption index 2	CAI	0,5(2020nm+2220nm)-2100nm
		Original Formula	9	3	4
23	Chlorophyll Absorption Ratio Index	CARI	(
700nm
670nm
)
sqrt(a*670+670nm+b)2
(a2+1)0.5
	b=(550nm-((700nm-550nm)/150*550)), a=(700nm-550nm)/150	Original Formula	30	3	4
24	Chlorophyll Absorption Ratio Index 2	CARI2	(
|(a*[670]+[670]+b)|
(a2+1)0.5
)(
[700]
[670]
)
	a=([700]-[550])/150, b=[550]-(a*[550])	Original Formula	30	3	1
25	Chlorophyll Green	Chlgreen	(
[760:800]
[540:560]
)(-1)
		Original Formula	79	3	1
26	Chlorophyll Index Green	CIgreen	
NIR
GREEN
-1
		Original Formula	86	3	3
27	Chlorophyll Index RedEdge 710	CIrededge710	
750nm
710nm
-1
		Original Formula	27	4	1
28	Chlorophyll IndexRedEdge	CIrededge	
NIR
rededge
-1
		Original Formula	69	4	3
29	Chlorophyll Red-Edge	Chlred-edge	(
[760:800]
[690:720]
)(-1)
		Original Formula	63	4	1
30	Chlorophyll vegetation index	CVI	NIR
RED
GREEN2
		Original Formula	82	3	2
31	Clay		
[2145:2185]*[2235:2365]
[2185:2225]*[2185:2225]
		Derived	13	3	1
32	Coloration Index	CI	
RED-BLUE
RED
		Original Formula	71	1	1
33	Corrected Transformed Vegetation Index	CTVI	
NDVI+0,5
|NDVI+0,5|
*sqrt|(NDVI)+0,5|
		Derived	85	1	1
34	CRI550	CRI550	[510](-1)-[550](-1)
		Original Formula	47	0	1
35	CRI700	CRI700	[510](-1)-[700](-1)
		Original Formula	33	0	1
36	Crop water stress index	CWSI	
C-A
B-A
		Original Formula	0	6	6
37	Curvative Index	CI	675nm
690nm
683nm2
		Original Formula	12	0	2
38	Datt1	Datt1	
850nm-710nm
850nm-680nm
		Original Formula	27	2	3
39	Datt4	Datt4	
672nm
550nm*708nm
		Original Formula	32	2	3
40	Datt6	Datt6	
860nm
550nm*708nm
		Original Formula	28	2	3
41	Difference 1725/970 Difference LAI	DLAI	1725nm-970nm
		Original Formula	16	2	1
42	Difference 678/500	D678/500	678nm-500nm
		Original Formula	59	0	1
43	Difference 800/550	D800/550	800nm-550nm
		Original Formula	62	2	2
44	Difference 800/680	D800/680	800nm-680nm
		Original Formula	66	2	2
45	Difference 833/658	D833/658	833nm-658nm
		Original Formula	63	0	1
46	Difference NIR/Green Green Difference Vegetation Index	GDVI	NIR-G
		Original Formula	86	1	1
47	Differenced Vegetation Index MSS	DVIMSS	2.4[800:1100]-[600:700]
		Original Formula	84	0	2
48	Disease water stress index	DSWI	
802nm+547nm
1657nm+682nm
		Original Formula	20	3	1
49	Disease-Water Stress Index 5	DSWI-5	
800nm-550nm
1660nm+680nm
		Original Formula	24	3	1
50	DmSR	DmSR	
DR(720nm)-DR(500nm)
DR(720nm)+DR(500nm)
		Original Formula	30	0	1
51	Dolomite		
[2185:2225]+[2295:2365]
[2235:2365]
		Derived	12	3	1
52	Double Difference Index	DD	(749nm-720nm)-(701nm-672nm)
		Original Formula	16	2	2
53	Double Peak Index	DPI	
688nm+710nm
697nm2
		Original Formula	16	3	2
54	Enhanced Vegetation Index	EVI	2.5
NIR-RED
(NIR+6RED-7.5BLUE)+1
		Original Formula	69	3	13
55	Enhanced Vegetation Index 2	EVI2	2.4
NIR-RED
NIR+RED+1
		Original Formula	87	0	1
56	Enhanced Vegetation Index 2 -2	EVI2	2.5
NIR-RED
NIR+2.4RED+1
		Original Formula	87	0	1
57	EPI	EPI	a
[672]
([550]*[708])b
		Original Formula	32	0	1
58	Epidote/Chlorite/Amphibole		
[2185:2225]+[2360:2430]
[2235:2365]+[2295:2365]
		Derived	12	2	0
59	Ferric iron, Fe2+	Fe2+	
[2145:2185]
[760:860]
+
[520:600]
[630:690]
		Derived	23	3	1
60	Ferric iron, Fe3+	Fe3+	
[630:690]
[520:600]
		Derived	84	3	1
61	Ferric Oxides		
[1600:1700]
[760:860]
		Derived	40	3	0
62	Ferrous iron		
[2145:2185]
[760:860]
+
[520:600]
[630:690]
		Derived	23	3	1
63	Ferrous Silicates		
[2145:2185]
[1600:1700]
		Derived	25	3	0
64	Gitelson2		(
750nm-800nm
695nm-740nm
)-1
		Original Formula	15	0	1
65	Global Environment Monitoring Index	GEMI	(n(1-0.25n)-
RED-0.125
1-RED
)
	n = ( 2 * ( NIR ^2 - RED ^2) + 1.5 * NIR + 0.5 * RED ) / ( NIR + RED + 0.5 )	Original Formula	87	1	11
66	Global Vegetation Moisture Index	GVMI	
(NIR+0.1)-(SWIR+0.02)
(NIR+0.1)+(SWIR+0.02)
		Original Formula	42	0	2
67	Gossan		
[1600:1700]
[630:690]
		Derived	40	1	1
68	Green atmospherically resistant vegetation index	GARI	
NIR-(GREEN-(BLUE-RED))
NIR-(GREEN+(BLUE-RED))
		Original Formula	67	0	2
69	Green leaf index	GLI	
2GREEN-RED-BLUE
2GREEN+RED+BLUE
		Original Formula	68	4	2
70	Green Normalized Difference Vegetation Index	GNDVI	
NIR-[540:570]
NIR+[540:570]
		Original Formula	86	1	13
71	Green Optimized Soil Adjusted Vegetation Index	GOSAVI	
NIR-G
NIR+G+Y
		Original Formula	86	2	0
72	Green Soil Adjusted Vegetation Index	GSAVI	
NIR-G
NIR+G+L
(1+L)
		Original Formula	86	2	0
73	Green-Blue NDVI	GBNDVI	
NIR-(GREEN+BLUE)
NIR+(GREEN+BLUE)
		Original Formula	68	1	1
74	Green-Red NDVI	GRNDVI	
NIR-(GREEN+RED)
NIR+(GREEN+RED)
		Original Formula	82	1	2
75	Greenness Above Bare Soil	GRABS	GVI-0.09178SBI+5.58959
		Original Formula	0	0	2
76	Host Rock		
[2145:2185]
[2185:2225]
		Derived	13	3	0
77	Hue	H	arctan(
2R-G-B
30.5
(G-B))
		Original Formula	68	1	1
78	Hyperspectral perpendicular VI	PVIhyp	
1148nm-a*807nm-b
(1+a2)0.5
	a=1.17, b=3.37	Original Formula	16	2	1
79	Ideal vegetation index	IVI	
NIR-b
a*RED
		Original Formula	87	1	1
80	Infrared percentage vegetation index	IPVI	
NIR
NIR+RED
2
(NDVI+1)
		Original Formula	82	1	2
81	Intensity	I	(
1
30.5
)(R+G+B)
		Original Formula	68	1	1
82	Inverse reflectance 550	IR550	550nm(-1)
		Original Formula	89	0	1
83	Inverse reflectance 700	IR700	700nm(-1)
		Original Formula	58	0	1
84	Kaolinitic		
[2235:2365]
[2145:2185]
		Derived	13	2	1
85	Laterite		
[1600:1700]
[2145:2185]
		Derived	25	2	1
86	Leaf Chlorophyll Index	LCI	
[850]-[710]
[850]+[680]
		Original Formula	27	3	2
87	Leaf Water Content Index	LWCI	
log(1-(NIR-MIDIR))
-log(1-(NIR-MIDIR))
		Original Formula	46	3	3
88	Log Ratio	LogR	log(
NIR
RED
)
		Derived	87	0	0
89	Maccioni		
780nm-710nm
780nm-680nm
		Original Formula	31	2	3
90	MCARI/MTVI2	MCARI/MTVI2	
((700nm-670nm)-0.2(700nm-550nm))(
700nm
670nm
)
(1.5
1.2(800nm-550nm)-2.5(670nm-550nm)
sqrt(2800nm+1)2-(6800nm-5sqrt670nm)-0.5
)
		Original Formula	23	2	2
91	MCARI/OSAVI	MCARI/OSAVI	
(700nm-670nm)-0.2(700nm-550nm)(
700nm
670nm
)
(1+0.16)
800nm-670nm
800nm+670nm+0.16
		Original Formula	23	0	4
92	MCARI/OSAVI750	MCARI/OSAVI750	
(750nm-705nm)-0.2(750nm-550nm)(
750nm
705nm
)
(1+0.16)
750nm-705nm
750nm+705nm+0.16
		Original Formula	24	0	1
93	MCARI2/OSAVI2	MCARI2/OSAVI2	
(
(
(
(
1.5
2.5(800nm-670nm)-1.3(800nm-550nm)
sqrt(2800nm+1)2-(6800nm-5sqrt670nm)-0.5
(1+0.16)
750nm-705nm
750nm+705nm+0.16
(
(
(
(
		Original Formula	18	0	1
94	mCRIG	mCRIG	([510:520](-1)-[560:570](-1))*NIR
		Original Formula	54	0	1
95	mCRIRE	mCRIRE	([510:520](-1)-[690:700](-1))*NIR
		Original Formula	55	0	1
96	MERIS Terrestrial chlorophyll index	MTCI	
754nm-709nm
709nm-681nm
		Original Formula	25	2	5
97	Mid-infrared vegetation index	MVI	
[700:1300]
[1570:1780]
		Original Formula	41	1	2
98	Misra Green Vegetation Index	MGVI	-0.386[500:600]-0.530[600:700]+0.535[700:800]+0.532[800:1100]
		Original Formula	44	0	2
99	Misra Non Such Index	MNSI	0.404[500:600]-0.039[600:700]-0.505[700:800]+0.762[800:1100]
		Original Formula	44	0	2
100	Misra Soil Brightness Index	MSBI	0.406[500:600]+0.600[600:700]+0.645[700:800]+0.243[800:1100]
		Original Formula	44	0	2
101	Misra Yellow Vegetation Index	MYVI	0.723[500:600]-0.597[600:700]+0.206[700:800]-0.278[800:1100]
		Original Formula	44	0	2
102	mND680	mND680	
800nm-680nm
800nm+680nm-2445nm
		Original Formula	32	0	1
103	Modified anthocyanin reflectance index	mARI	([530:570](-1)-[690:710](-1))*NIR
		Original Formula	65	0	2
104	Modified Chlorophyll Absorption in Reflectance Index	MCARI	((700nm-670nm)-0.2(700nm-550nm))(
700nm
670nm
)
		Original Formula	30	2	10
105	Modified Chlorophyll Absorption in Reflectance Index 1	MCARI1	1.2(2.5(800nm-670nm)-1.3(800nm-550nm))
		Original Formula	59	2	1
106	Modified Chlorophyll Absorption in Reflectance Index 1510	MCARI1510	((700nm-1510nm)-0.2(700nm-550nm))(
700nm
1510nm
)
		Original Formula	10	2	1
107	Modified Chlorophyll Absorption in Reflectance Index 2	MCARI2	(1.5
2.5(800nm-670nm)-1.3(800nm-550nm)
sqrt(2800nm+1)2-(6800nm-5sqrt670nm)-0.5
)
		Original Formula	59	2	2
108	Modified Chlorophyll Absorption Ratio Index 705,750	MCARI705	((750nm-705nm)-0.2(750nm-550nm))(
750nm
705
)
		Original Formula	24	2	1
109	Modified Chlorophyll Absorption Ratio Index 710	MCARI710	((750nm-710nm)-0.2(750nm-550nm))(
750nm
710
)
		Original Formula	25	2	1
110	Modified NDVI	mNDVI	
800nm-680nm
800nm+680nm-2445nm
		Original Formula	32	1	2
111	Modified Normalised Difference 734/747/715/726 Vogelmann indices 2	Vog2	
734nm-747nm
715nm+726nm
		Original Formula	13	2	8
112	Modified Normalised Difference 750/705	MND750/705	
750nm-705nm
750nm+705nm-2445nm
		Original Formula	21	2	4
113	Modified Normalized Difference 734/747/715/720	MD734/747/715/72	
734nm-747nm
715nm-720nm
		Original Formula	12	2	6
114	Modified Normalized Difference 850/1788/1928	ND850/1788/1928	
850nm?1788nm
850nm+1928nm
		Original Formula	8	0	1
115	Modified Normalized Difference 850/2218/1928	ND850/2218/1928	
850nm?2218nm
850nm+1928nm
		Original Formula	8	0	1
116	Modified Normalized Difference Vegetation Index RVI	MRVI	
RVI-1
RVI+1
		Original Formula	0	1	1
117	Modified Simple Ratio	mSR	
800nm-445nm
680nm-445nm
		Original Formula	32	1	3
118	Modified Simple Ratio 670,800	MSR670	
800nm
670nm
-1
sqrt
800nm
670nm
+1
		Original Formula	65	1	3
119	Modified Simple Ratio 705,750	MSR705	
750nm
705nm
-1
sqrt
750nm
705nm
+1
		Original Formula	27	0	1
120	Modified Simple Ratio 705/445	MSR705/445	
750nm-445nm
705nm-445nm
		Original Formula	21	2	4
121	Modified Simple Ratio NIR/RED	MSRNir/Red	
(
NIR
RED
)-1
sqrt(
NIR
RED
)+1
		Original Formula	87	0	3
122	Modified Soil Adjusted Vegetation Index	MSAVI	
2NIR+1-sqrt(2NIR+1)2-8(NIR-RED)
2
		Original Formula	87	1	8
123	Modified Soil Adjusted Vegetation Index hyper	MSAVIhyper	(0.5)((2800nm+1)-sqrt(2800nm+1)2-8(800nm-670nm))
		Original Formula	65	1	9
124	Modified Triangular Vegetation Index 1	MTVI1	1.2(1.2(800nm-550nm)-2.5(670nm-550nm))
		Original Formula	59	1	1
125	Modified Triangular Vegetation Index 2	MTVI2	(1.5
1.2(800nm-550nm)-2.5(670nm-550nm)
sqrt(2800nm+1)2-(6800nm-5sqrt670nm)-0.5
)
		Original Formula	59	1	3
126	Modifies NLI	MNLI	
(1760nm2-824nm)*1,5
1760nm2+824nm+0,5
		Original Formula	12	0	1
127	mSR2	mSR2	(
750nm
705nm
)-
1
sqrt(
750nm
705nm
)+1
		Original Formula	27	0	1
128	Muscovite		
[2235:2365]
[2185:2225]
		Derived	13	3	1
129	new Double Difference Index	DDn	2(710nm-760nm-760nm)
		Original Formula	28	0	2
130	Nonlinear vegetation index	NLI	
[780:1400]2-RED
[780:1400]2+RED
		Original Formula	87	0	3
131	Norm G	Norm G	
G
NIR+R+G
		Original Formula	82	1	0
132	Norm NIR	Norm NIR	
NIR
NIR+R+G
		Original Formula	82	1	0
133	Norm R	Norm R	
R
NIR+R+G
		Original Formula	82	1	0
134	Normalized Difference 1070/1200 NDWI-Hyperion	NDWI-Hyp	
1070nm-1200nm
1070nm+1200nm
		Original Formula	10	0	2
135	Normalized Difference 1080/1180	ND1080/1180	
1080nm-1180nm
1080nm+1180nm
		Original Formula	9	0	1
136	Normalized Difference 1080/1260	ND1080/1260	
1080nm-1260nm
1080nm+1260nm
		Original Formula	11	0	1
137	Normalized Difference 1080/1450	ND1080/1450	
1080nm-1450nm
1080nm+1450nm
		Original Formula	10	0	1
138	Normalized Difference 1080/1675	ND1080/1675	
1080nm-1675nm
1080nm+1675nm
		Original Formula	12	0	1
139	Normalized Difference 1080/2170	ND1080/2170	
1080nm-2170nm
1080nm+2170nm
		Original Formula	10	0	1
140	Normalized Difference 1094/1205 Leaf water VI 2	LWVI-2	
1094nm-1205nm
1094nm+1205nm
		Original Formula	9	2	1
141	Normalized Difference 1094/983 Leaf water VI 1	LWVI-1	
1094nm-893nm
1094nm+893nm
		Original Formula	11	2	1
142	Normalized Difference 1180/1450	ND1180/1450	
1180nm-1450nm
1180nm+1450nm
		Original Formula	9	0	1
143	Normalized Difference 1180/1675	ND1180/1675	
1180nm-1675nm
1180nm+1675nm
		Original Formula	11	0	1
144	Normalized Difference 1180/2170	ND1180/2170	
1180nm-2170nm
1180nm+2170nm
		Original Formula	10	0	1
145	Normalized Difference 1260/1450	ND1260/1450	
1260nm-1450nm
1260nm+1450nm
		Original Formula	9	0	1
146	Normalized Difference 1260/1675	ND1260/1675	
1260nm-1675nm
1260nm+1675nm
		Original Formula	13	0	1
147	Normalized Difference 1260/2170	ND1260/2170	
1260nm-2170nm
1260nm+2170nm
		Original Formula	12	0	1
148	Normalized Difference 1510/660 NRI1510	ND1510/660	
1510nm-660nm
1510nm+660nm
		Original Formula	13	0	1
149	Normalized Difference 2160/1540 Normalized Difference leaf canopy biomass	NDBleaf	
2160nm-1540nm
2160nm+1540nm
		Original Formula	11	2	0
150	Normalized Difference 2260/1490 Normalized Difference leaf mass per area	NDlma	
2260nm-1490nm
2260nm+1490nm
		Original Formula	10	2	1
151	Normalized Difference 415/435 Normalized Phaeophytinization Index , Normalized difference pigment index NDPI	NPQI	
415nm-435nm
415nm+435nm
		Original Formula	15	3	6
152	Normalized Difference 528/587 Photochemical Reflectance Index 528/587	PRI528/587	
528nm-567nm
528nm+567nm
		Original Formula	26	1	3
153	Normalized Difference 531/570 Photochemical Reflectance Index 531/570	PRI531/570	
531nm-570nm
531nm+570nm
		Original Formula	22	2	10
154	Normalized Difference 550/450 Plant pigment ratio	PPR	
550nm-450nm
550nm+450nm
		Original Formula	54	0	1
155	Normalized Difference 550/530 Physiological reflectance index	PRI550/530	
550nm-530nm
550nm+530nm
		Original Formula	27	0	1
156	Normalized Difference 550/531	ND550/531	
550nm-531nm
550nm+531nm
		Original Formula	22	0	1
157	Normalized Difference 550/650 Photosynthetic vigour ratio	PVR	
550nm-650nm
550nm+650nm
		Original Formula	64	0	1
158	Normalized Difference 570/531 Photochemical Reflectance Index 570/531	PRI570/531	
570nm-531nm
570nm+531nm
		Original Formula	22	1	4
159	Normalized Difference 570/539	ND570/539	
570nm-539nm
570nm+539nm
		Original Formula	18	0	1
160	Normalized Difference 680/430 Normalized Pigment Chlorophyll Index	NPCI	
680nm-430nm
680nm+430nm
		Original Formula	31	2	10
161	Normalized Difference 682/553	ND682/553	
682nm-553nm
682nm-553nm
		Original Formula	58	1	2
162	Normalized Difference 750/550 Green NDVI	NDVIg	
750nm-550nm
750nm+550nm
		Original Formula	37	1	1
163	Normalized Difference 750/650	NDVI750/650	
750nm-650nm
750nm+650nm
		Original Formula	31	0	1
164	Normalized Difference 750/660	ND750/660	
750nm?660nm
750nm+660nm
		Derived	37	0	1
165	Normalized Difference 750/680	ND750/680	
750nm-680nm
750nm+680nm
		Original Formula	37	0	1
166	Normalized Difference 750/705 Chl NDI	NDVI705	
750nm-705nm
750nm+705nm
		Original Formula	27	2	6
167	Normalized Difference 750/710 Red Edge NDVI	reNDVI	
750nm-710nm
750nm+710nm
		Original Formula	27	1	2
168	Normalized Difference 774/677	ND774/677	
774nm-677nm
774nm+677nm
		Original Formula	65	0	1
169	Normalized Difference 780/550 Green NDVI hyper	GNDVIhyper	
780nm-550nm
780nm+550nm
		Original Formula	65	2	2
170	Normalized Difference 782/666	ND782/666	
782nm-666nm
782nm+666nm
		Original Formula	72	0	1
171	Normalized Difference 790/670	ND790/670	
790nm-670nm
790nm+670nm
		Original Formula	69	2	1
172	Normalized Difference 790/720 Normalized difference red edge index	NDRE	
790nm-720nm
790nm+720nm
		Original Formula	30	1	2
173	Normalized Difference 800/1180	ND800/1180	
800nm-1180nm
800nm+1180nm
		Original Formula	10	0	1
174	Normalized Difference 800/1260	ND800/1260	
800nm-1260nm
800nm+1260nm
		Original Formula	14	0	1
175	Normalized Difference 800/1450	ND800/1450	
800nm-1450nm
800nm+1450nm
		Original Formula	11	0	1
176	Normalized Difference 800/1675	ND800/1675	
800nm-1675nm
800nm+1675nm
		Original Formula	28	0	1
177	Normalized Difference 800/2170	ND800/2170	
800nm-2170nm
800nm+2170nm
		Original Formula	21	0	0
178	Normalized Difference 800/470 Pigment specific normalised difference C2	PSNDc2	
800nm-470nm
800nm+470nm
		Original Formula	47	2	2
179	Normalized Difference 800/500 Pigment specific normalised difference C1	PSNDc1	
800nm-500nm
800nm+500nm
		Original Formula	53	2	1
180	Normalized Difference 800/550 Green NDVI hyper 2	GNDVIhyper2	
800nm-550nm
800nm+550nm
		Original Formula	62	1	1
181	Normalized Difference 800/635 Pigment specific normalised difference B2	PSNDb2	
800nm-635nm
800nm-635nm
		Original Formula	60	2	2
182	Normalized Difference 800/650 Pigment specific normalised difference B1	PSNDb1	
800nm-650nm
800nm+650nm
		Original Formula	62	2	1
183	Normalized Difference 800/675 Pigment specific normalised difference A1	PSNDa1	
800nm-675nm
800nm+675nm
		Original Formula	65	2	1
184	Normalized Difference 800/680 Pigment specific normalised difference A2, Lichtenthaler indices 1, NDVIhyper	ND800/680	
800nm-680nm
800nm+680nm
		Original Formula	66	9	10
185	Normalized Difference 819/1600 NDII	NDII	
819nm-1600nm
819nm+1600nm
		Original Formula	31	0	3
186	Normalized Difference 819/1649 NDII 2	NDII2	
819nm-1649nm
819nm+1649nm
		Original Formula	31	0	1
187	Normalized Difference 820/1600 Normalized Difference Moisture Index	NDMI	
820nm-1600nm
820nm+1600nm
		Original Formula	31	1	4
188	Normalized Difference 827/668	ND827/668	
827nm-668nm
827nm+668nm
		Original Formula	61	0	1
189	Normalized Difference 833/1649 Infrared Index	ND833/1649	
833nm-1649nm
833nm+1649nm
		Original Formula	30	0	1
190	Normalized Difference 833/658	ND833/658	
833nm-658nm
833nm+658nm
		Original Formula	63	0	1
191	Normalized Difference 850/1650 Normalized Difference Infrared Index	NDII	
850nm-1650nm
850nm+1650nm
		Original Formula	14	2	1
192	Normalized Difference 857/1241 Normalized Difference Water Index	NDWI2	
857nm-1241nm
857nm+1241nm
		Original Formula	17	2	1
193	Normalized Difference 860/1240 Normalized Difference Water Index	NDWI	
860nm-1240nm
860nm+1240nm
		Original Formula	16	2	9
194	Normalized Difference 860/1640	SIWSI	
860nm-1640nm
860nm+1640nm
		Original Formula	38	1	1
195	Normalized Difference 895/675	ND895/675	
895nm-675nm
895nm+675nm
		Original Formula	47	0	2
196	Normalized Difference 900/680	ND900/680	
900nm-680nm
900nm+680nm
		Original Formula	48	0	2
197	Normalized Difference 925/710 Normalized Difference Chlorophyll	NDchl	
925nm-710nm
925nm+710nm
		Original Formula	23	2	1
198	Normalized Difference 960/1180	ND960/1180	
960nm-1180nm
960nm+1180nm
		Original Formula	10	0	1
199	Normalized Difference 960/1260	ND960/1260	
960nm-1260nm
960nm+1260nm
		Original Formula	12	0	1
200	Normalized Difference 960/1450	ND960/1450	
960nm-1450nm
960nm+1450nm
		Original Formula	11	0	1
201	Normalized Difference 960/1675	ND960/1675	
960nm-1675nm
960nm+1675nm
		Original Formula	17	0	1
202	Normalized Difference 960/2170	ND960/2170	
960nm-2170nm
960nm+2170nm
		Original Formula	15	0	1
203	Normalized Difference Green/Red Normalized green red difference index, Visible Atmospherically Resistant Indices Green (VIgreen)	NGRDI	
GREEN-RED
GREEN+RED
		Original Formula	85	1	5
204	Normalized Difference Lignin Index	NDLI	
log(
1
1754nm
)-log(
1
1680nm
)
log(
1
1754nm
)+log(
1
1680nm
)
		Original Formula	10	1	1
205	Normalized Difference MIR/NIR Normalized Difference Vegetation Index (in case of strong atmospheric disturbances)	NDVI	
MIR-NIR
MIR+NIR
	MIR=[1300:3000],NIR=[800;10;10]	Original Formula	35	2	5
206	Normalized Difference NIR/Blue Blue-normalized difference vegetation index	BNDVI	
NIR-BLUE
NIR+BLUE
		Original Formula	71	1	3
207	Normalized Difference NIR/Green Green NDVI	GNDVI	
NIR-GREEN
NIR+GREEN
		Original Formula	86	2	5
208	Normalized Difference NIR/MIR Modified Normalized Difference Vegetation Index	MNDVI	
NIR-MIR
NIR+MIR
		Derived	42	1	2
209	Normalized Difference NIR/Red Normalized Difference Vegetation Index, Calibrated NDVI - CDVI	NDVI	
NIR-RED
NIR+RED
	RED=[670;50;30],NIR=[800;10;10]	Original Formula	71	13	116
210	Normalized Difference NIR/Rededge Normalized Difference Red-Edge	NDRE	
NIR-rededge
NIR+rededge
		Original Formula	69	1	3
211	Normalized Difference NIR/SWIR Normalized Burn Ratio	NBR	
NIR-SWIR
NIR+SWIR
		Original Formula	42	1	1
212	Normalized Difference Nitrogen Index	NDNI	
log(
1
1510nm
)-log(
1
1680nm
)
log(
1
1510nm
)+log(
1
1680nm
)
		Original Formula	11	4	2
213	Normalized Difference Red/Green Redness Index	RI	
R-G
R+G
		Original Formula	85	1	3
214	Normalized Difference Rededge/Red	NDVI rededge	
rededge-RED
rededge+RED
		Original Formula	31	2	2
215	Normalized Difference Salinity Index	NDSI	
[1600:1700]-[2145:2185]
[1600:1700]+[2145:2185]
		Derived	25	1	2
216	Normalized Difference Vegetation Index 690-710	NDVI690-710	
NIR-[690:710]
NIR+[690:710]
		Original Formula	69	3	1
217	Normalized Difference Vegetation Index C	NDVIc	
NIR-RED
NIR+RED
(1-
SWIR-SWIIRmin
SWIRmax-SWIRmin
)		Derived	41	0	1
218	Optimized Soil Adjusted Vegetation Index	OSAVI	(1+Y)
800nm-670nm
800nm+670nm+Y
	Y=0.16	Original Formula	65	1	12
219	Optimized Soil Adjusted Vegetation Index 1510	OSAVI1510	
(1+L)(800nm-1510nm)
800nm+1510nm+L
		Original Formula	12	1	1
220	Optimized Soil Adjusted Vegetation Index 2	OSAVI2	(1+0.16)
750nm-705nm
750nm+705nm+0.16
		Original Formula	27	1	1
221	Optimized vegetation normalized index	OVNI			Original Formula	0	0	1
222	Pan NDVI	PNDVI	
NIR-(GREEN+RED+BLUE)
NIR+(GREEN+RED+BLUE)
		Original Formula	67	1	1
223	Perpendicular Vegetation Index	PVI	(
1
sqrta2+1
)(NIR-ar-b)		Original Formula	46	1	18
224	Phengitic		
[2145:2185]
[2185:2225]
		Derived	13	2	1
225	Plant Senescence Reflectance Index	PSRI	
678nm-500nm
750nm
		Original Formula	25	1	3
226	Quartz Rich Rocks		
[10950:11650]
[8925:9275]
		Derived	5	3	1
227	Ratio 675/700/650	R675/700/650	
675nm
700nm*650nm
		Original Formula	17	2	2
228	Ratio Analysis of Reflectance Spectra A1	RARSa1	
675nm
700nm
r675
r700
		Original Formula	34	2	1
229	Ratio Analysis of Reflectance Spectra A2	RARSa2	
680nm
700nm
r680
r700
		Original Formula	35	2	1
230	Ratio Analysis of Reflectance Spectra A3	RARSa3	
675nm
800nm
r670
r800
		Original Formula	65	2	1
231	Ratio Analysis of Reflectance Spectra A4	RARSa4	
680nm
800nm
r680
r800
		Original Formula	66	2	1
232	Ratio Analysis of Reflectance Spectra B1	RARSb1	
675nm
650nm
*700nm
r650
r700
r675
		Original Formula	17	2	1
233	Ratio Analysis of Reflectance Spectra B2	RARSb2	
680nm
635nm
*700nm
r635
r700
r680
		Original Formula	19	2	1
234	Ratio Analysis of Reflectance Spectra B3	RARSb3	
675nm
650nm
*800nm
r650
r800
r675
		Original Formula	23	2	1
235	Ratio Analysis of Reflectance Spectra B4	RARSb4	
680nm
635nm
*800nm
r635
r800
r680
		Original Formula	23	2	1
236	Ratio Analysis of Reflectance Spectra C1	RARSc1	
760nm
500nm
r760
r500
		Original Formula	43	2	1
237	Ratio Analysis of Reflectance Spectra C2	RARSc2	
760nm
470nm
r760
r470
		Original Formula	41	2	1
238	Ratio Analysis of Reflectance Spectra C3	RARSc3	
800nm
500nm
r800
r500
		Original Formula	53	2	1
239	Ratio Analysis of Reflectance Spectra C4	RARSc4	
800nm
470nm
r800
r470
		Original Formula	47	1	1
240	Ratio of WI and Normalised Difference 750/660	WI/ND750	
900nm
970nm
750nm?705nm
750nm+705nm
		Original Formula	17	3	1
241	RDVI	RDVI	
800nm-670nm
(800nm+670nm)0.5
		Original Formula	65	1	4
242	RDVI2	RDVI2	
833nm-658nm
sqrt833nm+658nm
		Original Formula	63	1	1
243	Red edge 1	Rededge1	
[708:716]
[676:685]
		Original Formula	41	1	1
244	Red edge 2	Rededge2	
[708:716]-[676:685]
[708:716]+[676:685]
		Original Formula	41	1	1
245	Red-Blue NDVI	RBNDVI	
NIR-(RED+BLUE)
NIR+(RED+BLUE)
		Original Formula	69	1	1
246	Red-Edge Inflection Point 1	REIP1	700+40(
(
670nm+780nm
2
)-700nm
740nm-700nm
)		Original Formula	23	3	5
247	Red-Edge Inflection Point 2	REIP2	702+40(
(
667nm+782nm
2
)-702nm
742nm-702nm
)		Original Formula	21	3	4
248	Red-Edge Inflection Point 3	REIP3	705+35(
(
665nm+783nm
2
)-705nm
740nm-705nm
)		Original Formula	23	3	4
249	Red-Edge Position Linear Interpolation	REP	700+40
(
670nm+780nm
2
)-700nm
740nm-700nm
		Original Formula	24	1	5
250	Red-Edge Stress Vegetation Index	RVSI	
718nm+748nm
2
-733nm		Original Formula	17	2	0
251	Reduced Simple Ratio	RSR	
NIR
RED
*MIRmax-
MIR
MIRmax
-MIRmin		Original Formula	41	1	1
252	Reflectance at the inflexion point	Rre	
[670]+[780]
2
		Original Formula	72	0	1
253	Relative Drought Index	RDI	
WSDact
WSDcrit
		Original Formula	0	0	0
254	Relative Greenness Index	RGI			Original Formula	0	0	1
255	Relative Water Content Index	RWC	
FW-DW
TW-DW
		Original Formula	0	2	2
256	Renormalized Difference Vegetation Index	RDVI	
800nm-670nm
sqrt800nm+670nm
		Original Formula	65	2	7
257	Residual Moisture Index	RMI			Original Formula	0	0	1
258	RVSI	RVSI	
714nm+752nm
2
-733nm		Original Formula	18	0	1
259	Saturation	S	
max(R,G,B)-min(R,G,B)
max(R,G,B)
		Original Formula	0	1	1
260	SAVImir	SAVImir	(NIR-MIR)
1+L
NIR+MIR+L
		Original Formula	42	0	1
261	Sericite/Muscovite/Illite/Smecite		
[2145:2185]+[2235:2365]
[2185:2225]
		Derived	13	2	1
262	Shape Index	IF	
2R-G-B
G-B
		Original Formula	68	1	1
263	Silica 1		
[8475:8825]
[8125:8475]
		Derived	3	2	0
264	Silica 2		
[8475:8825]
[8925:9275]
		Derived	4	2	0
265	Silica 3		
[10250:10950]
[8125:8475]
		Derived	7	2	0
266	Silica 4		
[8475:8825]*[8475:8825]
[8125:8475]
[8925:9275]
		Derived	3	1	0
267	Siliceous Rocks		
[8475:8825]*[8475:8825]
[8125:8475]*[8925:9275]
		Derived	3	2	1
268	Simple Ratio 1058/1148	RVIhyp	
1058nm
1148nm
		Original Formula	11	1	1
269	Simple Ratio 1080/1180	SR1080/1180	
1080nm
1180nm
		Original Formula	9	0	1
270	Simple Ratio 1080/1260	SR1080/1260	
1080nm
1260nm
		Original Formula	11	0	1
271	Simple Ratio 1080/1450	SR1080/1450	
1080nm
1450nm
		Original Formula	10	0	1
272	Simple Ratio 1080/1675	SR1080/1675	
1080nm
1675nm
		Original Formula	12	0	1
273	Simple Ratio 1080/2170	SR1080/2170	
1080nm
2170nm
		Original Formula	10	0	1
274	Simple Ratio 1180/1080	SR1180/1080	
1180nm
1080nm
		Original Formula	9	0	1
275	Simple Ratio 1180/1450	SR1180/1450	
1180nm
1450nm
		Original Formula	9	0	1
276	Simple Ratio 1180/1675	SR1180/1675	
1180nm
1675nm
		Original Formula	11	0	1
277	Simple Ratio 1180/2170	SR1180/2170	
1180nm
2170nm
		Original Formula	10	0	1
278	Simple Ratio 1193/1126 Water content	WC	
1193nm
1126nm
		Original Formula	9	2	1
279	Simple Ratio 1250/1050 LAI determining index	LAIDI	
1250nm
1050nm
		Original Formula	14	3	0
280	Simple Ratio 1260/1080	SR1260/1080	
1260nm
1080nm
		Original Formula	11	0	1
281	Simple Ratio 1260/1450	SR1260/1450	
1260nm
1450nm
		Original Formula	9	0	1
282	Simple Ratio 1260/1675	SR1260/1675	
1260nm
1675nm
		Original Formula	13	0	1
283	Simple Ratio 1260/2170	SR1260/2170	
1260nm
2170nm
		Original Formula	12	0	1
284	Simple Ratio 1450/1080	SR1450/1080	
1450nm
1080nm
		Original Formula	10	0	1
285	Simple Ratio 1450/1180	SR1450/1180	
1450nm
1180nm
		Original Formula	9	0	1
286	Simple Ratio 1450/1260	SR1450/1260	
1450nm
1260nm
		Original Formula	9	0	1
287	Simple Ratio 1450/960	SR1450/960	
1450nm
960nm
		Original Formula	11	0	1
288	Simple Ratio 1599/819 Moisture Stress Index 2	MSI2	
1599nm
819nm
		Original Formula	29	0	1
289	Simple Ratio 1600/820 Moisture Stress Index	MSI	
1600nm
820nm
		Original Formula	31	2	7
290	Simple Ratio 1650/2218	TM5/TM7	
1650nm
2218nm
		Original Formula	23	0	1
291	Simple Ratio 1660/550 Disease-Water Stress Index 2	DSWI-2	
1660nm
550nm
		Original Formula	26	3	1
292	Simple Ratio 1660/680 Disease-Water Stress Index 3	DSWI-3	
1660nm
680nm
		Original Formula	28	3	1
293	Simple Ratio 1675/1080	SR1675/1080	
1675nm
1080nm
		Original Formula	12	0	1
294	Simple Ratio 1675/1180	SR1675/1180	
1675nm
1180nm
		Original Formula	11	0	1
295	Simple Ratio 1675/1260	SR1675/1260	
1675nm
1260nm
		Original Formula	13	0	1
296	Simple Ratio 1675/960	SR1675/960	
1675nm
960nm
		Original Formula	17	0	1
297	Simple Ratio 2170/1080	SR2170/1080	
2170nm
1080nm
		Original Formula	10	0	1
298	Simple Ratio 2170/1180	SR2170/1180	
2170nm
1180nm
		Original Formula	10	0	1
299	Simple Ratio 2170/1260	SR2170/1260	
2170nm
1260nm
		Original Formula	12	0	1
300	Simple Ratio 2170/960	SR2170/960	
2170nm
960nm
		Original Formula	15	0	2

Page 1 of 2 [1] [2] * > * >|

Index DataBase
A database for remote sensing indices
 Start | What is IDB? | How to use? | Credits | Contact | Feedback | 

Copyright © 2011-2026 by The IDB Project - All rights reserved • WebsiteInfo / Impressum / Datenschutz"
"List of available Indices
Order by: Name [^][v] • Abbreviation [^][v] • Applications [^][v] • Sensors [^][v] • References [^][v]

Page 2 of 2 |< * < * [1] [2]

Nr	Name	Abbrev.	Formula	Variables	Source	# Sens.	# Appl.	# Ref.
301	Simple Ratio 430/680 SRPI	SR430/680	
430nm
680nm
		Original Formula	31	2	4
302	Simple Ratio 440/690 Lichtenthaler indices 2	Lic2	
440nm
690nm
		Original Formula	33	2	3
303	Simple Ratio 440/740	SR440/740	
440nm
740nm
		Original Formula	28	0	2
304	Simple Ratio 450/550 Blue green pigment index	BGI	
450nm
550nm
		Original Formula	54	1	0
305	Simple Ratio 450/690 Blue red pigment index	BRI	
450nm
690nm
		Original Formula	49	1	0
306	Simple Ratio 520/420	SR520/420	
520nm
420nm
		Original Formula	27	0	1
307	Simple Ratio 520/670	SR520/670	
520nm
670nm
		Original Formula	63	0	1
308	Simple Ratio 520/760	SR520/760	
520nm
760nm
		Original Formula	48	0	1
309	Simple Ratio 542/750 Chl	SR542/750	
542nm
750nm
		Original Formula	29	0	1
310	Simple Ratio 550/420 Carter6	Ctr6	
550nm
420nm
		Original Formula	25	0	2
311	Simple Ratio 550/670	SR550/670	
550nm
670nm
		Original Formula	72	0	1
312	Simple Ratio 550/680 Disease-Water Stress Index 4	DSWI-4	
550nm
680nm
		Original Formula	70	3	1
313	Simple Ratio 550/760	SR550/760	
550nm
760nm
		Original Formula	47	0	1
314	Simple Ratio 550/800	SR550/800	
550nm
800nm
		Original Formula	62	2	1
315	Simple Ratio 554/677 Greenness Index	GI	
554nm
677nm
		Original Formula	71	2	5
316	Simple Ratio 556/750 Chl-b	SR556/750	
556nm
750nm
		Original Formula	40	0	1
317	Simple Ratio 560/658 GRVIhyper	SR560/658	
560nm
658nm
		Original Formula	70	1	1
318	Simple Ratio 605/420	SR605/420	
605nm
420nm
		Original Formula	21	0	2
319	Simple Ratio 605/670	SR605/670	
605nm
670nm
		Original Formula	29	0	2
320	Simple Ratio 605/760 Carter3	Ctr3	
605nm
760nm
		Original Formula	29	2	3
321	Simple Ratio 672/550 Datt5	SR672/550	
672nm
550nm
		Original Formula	71	2	3
322	Simple Ratio 672/708	SR672/708	
672nm
708nm
		Original Formula	38	0	1
323	Simple Ratio 674/553	SR674/553	
674nm
553nm
		Original Formula	73	0	1
324	Simple Ratio 675/555	SR675/555	
675nm
555nm
		Original Formula	73	0	1
325	Simple Ratio 675/700	SR675/700	
675nm
700nm
		Original Formula	34	2	3
326	Simple Ratio 675/705	SR675/705	
675nm
705nm
		Original Formula	36	0	1
327	Simple Ratio 678/750	SR678/750	
678nm
750nm
		Original Formula	36	0	1
328	Simple Ratio 683/510	SR683/510	
683nm
510nm
		Original Formula	47	2	1
329	Simple Ratio 685/735	SR685/735	
685nm
735nm
		Original Formula	31	0	2
330	Simple Ratio 690/735 Fluorescence ratio	FR	
690nm
735nm
		Original Formula	30	2	2
331	Simple Ratio 690/740 Fluorescence ratio 2	FR2	
690nm
740nm
		Original Formula	30	2	1
332	Simple Ratio 694/840	SR694/840	
694nm
840nm
		Original Formula	31	0	2
333	Simple Ratio 695/420 Carter1	Ctr1	
695nm
420nm
		Original Formula	23	3	7
334	Simple Ratio 695/670 Carter5	Ctr5	
695nm
670nm
		Original Formula	29	2	3
335	Simple Ratio 695/760 Carter2	Ctr2	
695nm
760nm
		Original Formula	33	3	8
336	Simple Ratio 695/800	SR695/800	
695nm
800nm
		Original Formula	32	0	1
337	Simple Ratio 700	SR700	
1
700nm
		Original Formula	58	2	3
338	Simple Ratio 700/670	SR700/670	
700nm
670nm
		Original Formula	37	2	3
339	Simple Ratio 705/722	D2	
705nm
722nm
		Original Formula	17	0	1
340	Simple Ratio 706/750 Chl-a	SR706/750	
706nm
750nm
		Original Formula	27	2	1
341	Simple Ratio 710/420	SR710/420	
710nm
420nm
		Original Formula	23	0	2
342	Simple Ratio 710/670	SR710/670	
710nm
670nm
		Original Formula	39	0	1
343	Simple Ratio 710/760 Carter4	Ctr4	
710nm
760nm
		Original Formula	28	2	3
344	Simple Ratio 715/705	SR715/705	
[710:720]
[700:710]
		Original Formula	21	2	3
345	Simple Ratio 715/705 Vogelmann indices 3	Vog3	
715nm
705nm
		Original Formula	19	2	5
346	Simple Ratio 730/706	D1	
730nm
706nm
		Original Formula	19	0	1
347	Simple Ratio 735/710	SR735/710	
735nm
[700:710]
		Original Formula	25	2	1
348	Simple Ratio 740/720	Vog1	
[734:747]
[715:726]
		Original Formula	24	2	2
349	Simple Ratio 740/720 hyper Vogelmann indices 1	Vog1hyper	
740nm
720nm
		Original Formula	21	2	5
350	Simple Ratio 750/550 Gitelson and Merzlyak 1	SR750/550	
750nm
550nm
		Original Formula	37	2	9
351	Simple Ratio 750/555	SR750/555	
750nm
555nm
		Original Formula	39	2	1
352	Simple Ratio 750/700 Gitelson and Merzlyak 2	SR750/700	
750nm
700nm
		Original Formula	30	2	10
353	Simple Ratio 750/705	SR750/705	
750nm
705nm
		Original Formula	27	0	5
354	Simple Ratio 750/710 Zarco-Tejada & Miller (ZM)	SR750/710	
750nm
710nm
		Original Formula	27	2	5
355	Simple Ratio 752/690	SR752/690	
752nm
690nm
		Original Formula	28	0	1
356	Simple Ratio 754/704 Datt3	Datt3	
754nm
704nm
		Original Formula	24	2	3
357	Simple Ratio 760/500 Ratio Analysis of Reflectance Spectra	RARS	
760nm
500nm
		Original Formula	43	0	1
358	Simple Ratio 760/695	SR760/695	
760nm
695nm
		Original Formula	32	0	1
359	Simple Ratio 774/677	SR774/677	
774nm
677nm
		Original Formula	65	0	1
360	Simple Ratio 800/1180	SR800/1180	
800nm
1180nm
		Original Formula	10	0	1
361	Simple Ratio 800/1280	SR800/1280	
800nm
1280nm
		Original Formula	13	0	1
362	Simple Ratio 800/1450	SR800/1450	
800nm
1450nm
		Original Formula	11	0	1
363	Simple Ratio 800/1660 Disease-Water Stress Index 1	DSWI-1	
800nm
1660nm
		Original Formula	28	3	1
364	Simple Ratio 800/1675	SR800/1675	
800nm
1675nm
		Original Formula	28	0	1
365	Simple Ratio 800/2170	SR800/2170	
800nm
2170nm
		Original Formula	21	0	1
366	Simple Ratio 800/470 Pigment specific simple ratio C2	PSSRc2	
800nm
470nm
		Original Formula	47	2	3
367	Simple Ratio 800/500 Pigment specific simple ratio C1	PSSRc1	
800nm
500nm
		Original Formula	53	2	2
368	Simple Ratio 800/550	SR800/550	
800nm
550nm
		Original Formula	62	3	4
369	Simple Ratio 800/600	SR800/600	
800nm
600nm
		Original Formula	42	1	2
370	Simple Ratio 800/635 Pigment Specific Simple Ratio (Cholophyll b) (PSSRb)	SR800/635	
800nm
635nm
		Original Formula	60	2	5
371	Simple Ratio 800/650 Pigment specific simple ratio B1	PSSRb1	
800nm
650nm
		Original Formula	62	2	2
372	Simple Ratio 800/670 Ratio Vegetation Index	RVI	
800nm
670nm
		Original Formula	65	1	20
373	Simple Ratio 800/675 Pigment specific simple ratio A1	PSSRa1	
800nm
675nm
		Original Formula	65	2	3
374	Simple Ratio 800/680 Pigment Specific Simple Ratio (Cholophyll a) (PSSRa)	SR800/680	
800nm
680nm
		Original Formula	66	2	8
375	Simple Ratio 800/960	SR800/960	
800nm
960nm
		Original Formula	21	0	1
376	Simple Ratio 801/550 NIR/Green	SR801/550	
801nm
550nm
		Original Formula	60	1	1
377	Simple Ratio 801/670 NIR/Red	SR801/670	
801nm
670nm
		Original Formula	65	1	1
378	Simple Ratio 810/560 Plant biochemical index	PBI	
810nm
560nm
		Original Formula	61	1	0
379	Simple Ratio 833/1649 MSIhyper	SR833/1649	
833nm
1649nm
		Original Formula	30	1	1
380	Simple Ratio 833/658	SR833/658	
833nm
658nm
		Original Formula	63	0	1
381	Simple Ratio 850/710 Datt2	Datt2	
850nm
710nm
		Original Formula	32	0	1
382	Simple Ratio 860/1240	SRWI	
860nm
1240nm
		Original Formula	16	1	1
383	Simple Ratio 860/550	SR860/550	
860nm
550nm
		Original Formula	64	0	1
384	Simple Ratio 860/708	SR860/708	
860nm
708nm
		Original Formula	34	0	1
385	Simple Ratio 895/972 Water band index 4	WBI4	
895nm
972nm
		Original Formula	21	3	1
386	Simple Ratio 900/680	SR900/680	
900nm
680nm
		Original Formula	48	0	1
387	Simple Ratio 950/900 Water band index	WBI3	
950nm
900nm
		Original Formula	21	3	2
388	Simple Ratio 960/1180	SR960/1180	
960nm
1180nm
		Original Formula	10	0	1
389	Simple Ratio 960/1260	SR960/1260	
960nm
1260nm
		Original Formula	12	0	1
390	Simple Ratio 960/1450	SR960/1450	
960nm
1450nm
		Original Formula	11	0	1
391	Simple Ratio 960/1675	SR960/1675	
960nm
1675nm
		Original Formula	17	0	1
392	Simple Ratio 960/2170	SR960/2170	
960nm
2170nm
		Original Formula	15	0	1
393	Simple Ratio 970/900 Plant Water Index, Water Band Index (WBI), Water Index (WI)	PWI	
970nm
900nm
		Original Formula	20	3	13
394	Simple Ratio 970/902 Water band index	WBI	
970nm
902nm
		Original Formula	19	3	1
395	Simple Ratio MIR/NIR Ratio Drought Index	RDI	
MIR
NIR
		Original Formula	42	1	1
396	Simple Ratio MIR/Red Eisenhydroxid-Index	SRMIR/Red	
MIR
RED
		Original Formula	41	2	0
397	Simple Ratio MIR/SWIR Cley Mineral-Index, Salinity Index	SI	
MIR
SWIR
		Original Formula	20	1	0
398	Simple Ratio NIR/700-715	SRNir/700-715	
NIR
[700:715]
		Original Formula	45	1	1
399	Simple Ratio NIR/G Green Ratio Vegetation Index	GRVI	
NIR
G
		Original Formula	86	1	1
400	Simple Ratio NIR/MIR	SRNIR/MIR	
NIR
MIR
		Original Formula	42	0	1
401	Simple Ratio NIR/RED Difference Vegetation Index, Vegetation Index Number (VIN)	DVI	
NIR
RED
		Original Formula	87	8	26
402	Simple Ratio NIR/Rededge RedEdge Ratio Index 1	RRI1	
NIR
rededge
		Original Formula	69	1	1
403	Simple Ratio Pigment Index	SRPI	
430nm
680nm
		Original Formula	31	1	0
404	Simple Ratio Red/Blue Iron Oxide	IO	
RED
BLUE
		Original Formula	71	3	1
405	Simple Ratio Red/Green Red-Green Ratio	RGR	
RED
GREEN
		Original Formula	85	0	1
406	Simple Ratio Red/NIR Ratio Vegetation-Index	SRRed/NIR	
RED
NIR
		Original Formula	87	0	2
407	Simple Ratio Rededge/Red RedEdge Ratio Index 2	RRI2	
rededge
RED
		Original Formula	31	1	1
408	Simple Ratio SWIRI/NIR Ferrous Minerals	SRSWIRI/NIR	
SWIRI
NIR
		Original Formula	46	1	0
409	Simple Ratio SWIRI/SWIRII Clay Minerals	SRSWIRI/SWIRII	
SWIRI
SWIRII
		Original Formula	0	2	0
410	Simple Ration 355 / 365 gk		(
355nm
l
*365nm)
	l=1.1	Derived	2	0	0
411	Single Band 1020	SB1020	1020nm
		Original Formula	28	2	1
412	Single Band 1040	SB1040	1040nm
		Original Formula	24	2	1
413	Single Band 1120	SB1120	1120nm
		Original Formula	16	2	1
414	Single Band 1200	SB1200	1200nm
		Original Formula	16	5	1
415	Single Band 1400	SB1400	1400nm
		Original Formula	14	2	1
416	Single Band 1420	SB1420	1420nm
		Original Formula	15	2	1
417	Single Band 1450	SB1450	1450nm
		Original Formula	14	5	1
418	Single Band 1490	SB1490	1490nm
		Original Formula	15	3	1
419	Single Band 1510	SB1510	1510nm
		Original Formula	16	3	2
420	Single Band 1530	SB1530	1530nm
		Original Formula	16	2	1
421	Single Band 1540	SB1540	1540nm
		Original Formula	16	3	1
422	Single Band 1580	SB1580	1580nm
		Original Formula	38	3	1
423	Single Band 1690	SB1690	1690nm
		Original Formula	31	5	1
424	Single Band 1780	SB1780	1780nm
		Original Formula	15	4	1
425	Single Band 1788	SB1788	1788nm
		Original Formula	14	0	2
426	Single Band 1820	SB1820	1820nm
		Original Formula	11	2	1
427	Single Band 1900	SB1900	1900nm
		Original Formula	10	2	1
428	Single Band 1940	SB1940	1940nm
		Original Formula	12	7	1
429	Single Band 1960	SB1960	1960nm
		Original Formula	13	3	1
430	Single Band 1980	SB1980	1980nm
		Original Formula	13	2	1
431	Single Band 2000	SB2000	2000nm
		Original Formula	13	2	1
432	Single Band 2060	SB2060	2060nm
		Original Formula	13	3	1
433	Single Band 2080	SB2080	2080nm
		Original Formula	18	3	1
434	Single Band 2100	SB2100	2100nm
		Original Formula	20	3	1
435	Single Band 2130	SB2130	2130nm
		Original Formula	24	2	1
436	Single Band 2180	SB2180	2180nm
		Original Formula	24	3	1
437	Single Band 2218	SB2218	2218nm
		Original Formula	24	0	1
438	Single Band 2240	SB2240	2240nm
		Original Formula	24	2	1
439	Single Band 2250	SB2250	2250nm
		Original Formula	25	2	1
440	Single Band 2270	SB2270	2270nm
		Original Formula	26	3	1
441	Single Band 2280	SB2280	2280nm
		Original Formula	26	3	1
442	Single Band 2300	SB2300	2300nm
		Original Formula	24	3	1
443	Single Band 2310	SB2310	2310nm
		Original Formula	22	2	1
444	Single Band 2320	SB2320	2320nm
		Original Formula	21	2	1
445	Single Band 2340	SB2340	2340nm
		Original Formula	20	2	1
446	Single Band 2350	SB2350	2350nm
		Original Formula	21	4	1
447	Single Band 430	SB430	430nm
		Original Formula	38	2	1
448	Single Band 460	SB460	460nm
		Original Formula	65	2	1
449	Single Band 470 Blackburn3	BB3	470nm
		Original Formula	64	2	1
450	Single Band 495	SR495	495nm
		Original Formula	73	0	1
451	Single Band 550	SB550	550nm
		Original Formula	89	2	6
452	Single Band 555	SB555	555nm
		Original Formula	94	0	1
453	Single Band 635 Blackburn2	BB2	635nm
		Original Formula	84	2	2
454	Single Band 640	SB640	640nm
		Original Formula	81	2	1
455	Single Band 655	SB655	655nm
		Original Formula	88	0	1
456	Single Band 660	SB660	660nm
		Original Formula	90	2	1
457	Single Band 670	SB670	670nm
		Original Formula	95	0	2
458	Single Band 675	SB675	675nm
		Original Formula	90	0	1
459	Single Band 680 Blackburn1	BB1	680nm
		Original Formula	93	2	3
460	Single Band 700	SB700	700nm
		Original Formula	58	0	1
461	Single Band 703 Boochs	SB703	703nm
		Original Formula	57	2	3
462	Single Band 705	SB705	705nm
		Original Formula	59	0	1
463	Single Band 720 Boochs2	SB720	720nm
		Original Formula	51	2	3
464	Single Band 735	SB735	735nm
		Original Formula	54	0	0
465	Single Band 801	SB801	801nm
		Original Formula	81	0	1
466	Single Band 850	SB850	850nm
		Original Formula	83	0	1
467	Single Band 885	SB885	885nm
		Original Formula	72	0	1
468	Single Band 910	SB910	910nm
		Original Formula	42	2	1
469	Single Band 930	SB930	930nm
		Original Formula	38	2	1
470	Single Band 970	SB970	970nm
		Original Formula	33	2	1
471	Single Band 990	SB990	990nm
		Original Formula	31	2	1
472	SiO2		
[10250:10950]
[8925:9275]
		Derived	5	1	0
473	sLAIDI	sLAIDI	S
1050nm-1250nm
1050nm+1250nm
	S=5	Original Formula	14	0	0
474	Soil Adjusted Vegetation Index	SAVI	
800nm-670nm
800nm+670nm+L
(1+L)
	L = 0,5	Original Formula	65	4	43
475	Soil and Atmospherically Resistant Vegetation Index	SARVI	(1+L)
800nm-(Rr-y(RB-Rr))
800nm+-(Rr-y(RB-Rr))+L
		Original Formula	81	2	7
476	Soil and Atmospherically Resistant Vegetation Index 2	SARVI2	2,5
NIR-RED
1+NIR+6RED-7,5BLUE
		Original Formula	69	0	2
477	Soil and Atmospherically Resistant Vegetation Index 3	SAVI3	(1+0,5)
833nm-658nm
833nm+658nm+0,5
		Original Formula	63	0	1
478	Soil Background Line	SBL	[800:1100]-2.4[600:700]
		Original Formula	84	0	2
479	Soil Composition Index		
[1600:1700]-[760:860]
[1600:1700]+[760:860]
		Derived	40	1	1
480	Soil-adjusted vegetation index 2	SAVI2	
NIR
RED+
b
a
		Original Formula	87	0	5
481	Specific Leaf Area Vegetation Index	SLAVI	
NIR
RED+SWIR
		Original Formula	41	1	1
482	Spectral Polygon Vegetation Index	SPVI	0.4(3.7(800nm-670nm)-1.2|530nm-670nm|)
		Original Formula	56	1	1
483	SQRT(IR/R)	SQRT(IR/R)	sqrt
NIR
RED
		Original Formula	87	0	0
484	Stress Index	SI			Original Formula	0	0	1
485	Structure Intensive Pigment Index 1	SIPI1	
800nm-445nm
800nm-680nm
		Original Formula	32	2	10
486	Structure Intensive Pigment Index 2	SIPI2	
800nm-505nm
800nm-690nm
		Original Formula	42	2	2
487	Structure Intensive Pigment Index 3	SIPI3	
800nm-470nm
800nm-680nm
		Original Formula	46	2	2
488	Tasselled Cap - brightness	SBI	0.3037[450:520]+0.2793[520:600]+0.4743[630:690]+0.5585[760:900]+0.5082[1150:1750]+0.1863[2080:2350]
		Original Formula	24	1	7
489	Tasselled Cap - Green Vegetation Index MSS	GVIMSS	-0.283[500:600]-0.660[600:700]+0.577[700:800]+0.388[800:1100]
		Original Formula	44	0	2
490	Tasselled Cap - Non Such Index MSS	NSIMSS	-0.016[500:600]+0.131[600:700]-0.425[700:800]+0.882[800:1100]
		Original Formula	44	0	2
491	Tasselled Cap - nonesuch				Derived	0	0	4
492	Tasselled Cap - Soil Brightness Index MSS	SBIMSS	0.332[500:600]+0.603[600:700]+0.675[700:800]+0.262[800:1100]
		Original Formula	44	0	2
493	Tasselled Cap - vegetation	GVI	-0.2848[450:520]-0.2435[520:600]-0.5436[630:690]+0.7243[760:900]+0.0840[1550:1750]-0.1800[2080:2350]
		Original Formula	24	1	13
494	Tasselled Cap - wetness	WET	0.1509[450:520]+0.1973[520:600]+0.3279[630:690]+0.3406[760:900]-0.7112[1550:1750]-0.4572[2080:2350]
		Original Formula	24	1	7
495	Tasselled Cap - Yellow Vegetation Index MSS	YVIMSS	-0.899[500:600]+0.428[600:700]+0.076[700:800]-0.041[800:1100]
		Original Formula	44	0	2
496	TCARI/OSAVI	TCARI/OSAVI	
3(700nm-670nm)-0.2(700nm-550nm)
700nm
670nm
(1+0.16)
800nm-670nm
800nm+670nm+0.16
		Original Formula	23	0	9
497	TCARI/OSAVI 705,750	TCARI/OSAVI705	
3(750nm-705nm)-0.2(750nm-550nm)(
750nm
705nm
)
(1+0.16)
750nm-705nm
750nm+705nm+0.16
		Original Formula	24	0	2
498	TCARI1510/OSAVI1510	TCARI1510/OSAVI1	
3((700nm-1510nm)-0,2(700nm-550nm)(
700nm
1510nm
))
(1+L)(800nm-1510nm)
800nm+1510nm+L
		Original Formula	10	0	1
499	Three-Band Ratio 1200	RATIO1200	2
[1180:1220]
[1090:1110]+([1265:1285])
		Original Formula	10	1	1
500	Three-Band Ratio 975	RATIO975	2
[960:990]
[920:940]+[1090:1110]
		Original Formula	9	2	1
501	Transformed Chlorophyll Absorbtion Ratio	TCARI	3((700nm-670nm)-0.2(700nm-550nm)(
700nm
670nm
))
		Original Formula	30	1	9
502	Transformed Chlorophyll Absorbtion Ratio 1510	TCARI1510	3((700nm-1510nm)-0,2(700nm-550nm)(
700nm
1510nm
))
		Original Formula	10	0	1
503	Transformed Chlorophyll Absorbtion Ratio 2	TCARI2	3((750nm-705nm)-0,2(750nm-550nm)(
750nm
705nm
))
		Original Formula	24	1	1
504	Transformed NDVI	TNDVI	sqrt
NIR-RED
NIR+RED
+0.5
		Original Formula	87	0	0
505	Transformed Soil Adjusted Vegetation Index	TSAVI	
B(NIR-B*R-A)
RED+B(NIR-A)+X(1+B2)
	B=B	Original Formula	87	4	14
506	Transformed Soil Adjusted Vegetation Index 2	TSAVI	
a*NIR-a*RED-b
RED+a*NIR-a*b
		Original Formula	87	1	4
507	Transformed Vegetation Index	TVI	sqrt(NDVI)+0,5
		Original Formula	85	1	2
508	Triangular chlorophyll index	TCI	1.2(700nm-550nm)-1.5(670nm-550nm)*sqrt
700nm
670nm
		Original Formula	30	2	1
509	Triangular greenness index	TGI	?0.5(([665:675]?[475:485])*(670nm?550nm)?([665:675]?[545:555])(670nm?480nm))
		Original Formula	4	0	1
510	Triangular Vegetation Index	TVI	0.5(120(750nm-550nm)-200(670nm-550nm))
		Original Formula	32	2	8
511	Vegetation Condition Index	VCI	
NDVIj-NDVImin
NDVImax-NDVImin
*100
		Original Formula	0	2	0
512	Vegetation Index 700	VI700	
700nm-[660:680]
700nm+[660:680]
		Original Formula	38	0	1
513	Visible Atmospherically Resistant Index Green	VARIgreen	
[545:565]-[620:680]
[545:565]+[620:680]-[459:490]
		Original Formula	67	0	4
514	Visible Atmospherically Resistant Indices 700	VARI700	
[700]-1,7[660:680]+0,7[470:490]
[700]+2,3[660:680]-1,3[470:490]
		Original Formula	31	0	2
515	Visible Atmospherically Resistant Indices RedEdge	VARIrededge	
[700:710]-[620:680]
[700:710]+[620:680]
		Original Formula	41	2	3
516	Weighted Difference Vegetation Index	WDVI	NIR-a*RED
		Original Formula	87	1	11
517	WI/NDVI	WI/NDVI	
900nm
970nm
800nm-680nm
800nm+680nm
		Original Formula	15	2	1
518	Wide Dynamic Range Vegetation Index	WDRVI	
0.1NIR-RED
0.1NIR+RED
		Original Formula	87	2	4
519	Yellowness index	YI	-10
580nm-2624nm+668nm
44nm2
		Original Formula	0	0	1

Page 2 of 2 |< * < * [1] [2]

Index DataBase
A database for remote sensing indices
 Start | What is IDB? | How to use? | Credits | Contact | Feedback | 

Copyright © 2011-2026 by The IDB Project - All rights reserved • WebsiteInfo / Impressum / Datenschutz"
"Calculating vegetation indices


Vegetation indices are simple equations that compare reflectances at different light wavelengths. One of the most common vegetation indices, the Normalized Difference Vegetation Index (NDVI), can be calculated directly in Pix4D, and the next protocol will continue with that data. If you are working with this data, you can skip ahead to the next lesson. If want to calculate other vegetation indices, read on.

There are many vegetation indices, and they are used to understand plant health, stress responses, and to separate vegetation from soil, for example.

Imagine a healthy plant. It's dark green, right? That's because it is reflecting very little blue or red light, but some green. An unhealthy plant might be yellow, and it would have more of those other wavelengths reflected. Therefore, making a simple equation like this might tell you something about plant health:

Green reflectance

_______________________


Red + Green + Blue reflectance



For a healthy plant, nearly all the light reflected is green, so it would have a high value. An unhealthy plant is reflecting those other wavelengths, so it would have a lower value. We can do calculations like this in QGIS using the "Raster Calculator". We could make a slightly more robust version of the equation above to study canopy health using RGB imagery:

Excess Green (ExG):


The equation for Excess Green is:
2 * (Green / (Red + Green + Blue)) - (Red / (Red + Green + Blue)) - (Blue / (Red + Green + Blue))


VARI:


The equation for VARI is:
(Green - Red) / (Green + Red - Blue)

For this exercise, we will continue using ExG.

Load some reflectance maps into your project. If importing from Pix4D, it is best to do this from the 4_index folder, rather than 3_dsm_mosaic.

Go to Raster -> Raster calculator.

To the right of "Output Layer", click the three dots and choose where to save your outputs.

Click on the layers you want to use to calculate. Add symbols by typing them in the box at bottom with your keyboard, or clicking the provided keys with your mouse

 

Bonus note: If you are using RGB data, index maps are certainly recommended. If you have no choice but to use the RGB orthomosaics, the data is stored in separate bands of a single file accordingly, and you may have to type this in manually:

Red    =   IMAGE_NAME@1

Green  =   IMAGE_NAME@2

Blue    =   IMAGE_NAME@3

To calculate ExG, your expression should look something like this: 

2*(\"2024-09-06 RGB_index_green@1\"/(\"2024-09-06 RGB_index_red@1\" + \"2024-09-06 RGB_index_green@1\" + \"2024-09-06 RGB_index_blue@1\"))

- (\"2024-09-06 RGB_index_red@1\"/(\"2024-09-06 RGB_index_red@1\" + \"2024-09-06 RGB_index_green@1\" + \"2024-09-06 RGB_index_blue@1\"))

- (\"2024-09-06 RGB_index_blue@1\"/(\"2024-09-06 RGB_index_red@1\" + \"2024-09-06 RGB_index_green@1\" + \"2024-09-06 RGB_index_blue@1\"))

Click OK.

After a few seconds, the new band will appear in your layers panel and interface. It should look something like this:

8. Keep in mind that this is a flexible process. There are many vegetation indices. Consider calculating a few and use what works best for you!

Optional: Making your vegetation index map look more awesome
Right click name of project in layers panel at bottom left.
Click "Properties".
Click "Symbology" (at left).
Change render type to "Singleband pseudocolor."
To the far right of "Color Ramp", click the drop-down arrow. You may want to then click "All color ramps". Change color to "RdYGn", "Inferno", or whatever you prefer.

Change "Mode" to "Equal interval" and "Classes" to "10" or more.
Click "OK."
See what you think. Consider going back into the Symbology and adjusting the Min and Max values. This is just an artistic representation. Your actual values are not affected. Do what looks good."
