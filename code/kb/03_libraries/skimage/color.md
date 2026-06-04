# scikit-image Color Space Conversion (skimage.color)

Source: https://scikit-image.org/docs/stable/api/skimage.color.html

Color space conversion.

## Functions

### `combine_stains(stains, conv_matrix, *, channel_axis=-1)`
Stain to RGB color space conversion.

**Parameters:**
- `stains` (…, C=3, …) array_like: Image in stain color space; final dimension denotes channels by default
- `conv_matrix` ndarray: Stain separation matrix as described by G. Landini
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `out` (…, C=3, …) ndarray: Image in RGB format, same dimensions as input

**Raises:**
- ValueError: If `stains` is not at least 2-D with shape (…, C=3, …)

**Notes:**
Stain combination matrices available in the `color` module: `rgb_from_hed`, `rgb_from_hdx`, `rgb_from_fgx`, `rgb_from_bex`, `rgb_from_rbd`, `rgb_from_gdx`, `rgb_from_hax`, `rgb_from_bro`, `rgb_from_bpx`, `rgb_from_ahx`, `rgb_from_hpx`

---

### `convert_colorspace(arr, fromspace, tospace, *, channel_axis=-1)`
Convert image array to new color space.

Valid color spaces: 'RGB', 'HSV', 'RGB CIE', 'XYZ', 'YUV', 'YIQ', 'YPbPr', 'YCbCr', 'YDbDr'

**Parameters:**
- `arr` (…, C=3, …) array_like: Image to convert; final dimension denotes channels by default
- `fromspace` str: Source color space (case-insensitive)
- `tospace` str: Target color space (case-insensitive)
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `out` (…, C=3, …) ndarray: Converted image, same dimensions as input

**Raises:**
- ValueError: If fromspace or tospace invalid

**Notes:** Conversion performed through RGB "central" color space, i.e. conversion from XYZ to HSV is implemented as XYZ -> RGB -> HSV instead of directly.

---

### `deltaE_cie76(lab1, lab2, channel_axis=-1)`
Euclidean distance between two points in Lab color space.

**Parameters:**
- `lab1` array_like: Reference color (Lab colorspace)
- `lab2` array_like: Comparison color (Lab colorspace)
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `dE` array_like: Distance between colors `lab1` and `lab2`

---

### `deltaE_ciede2000(lab1, lab2, kL=1, kC=1, kH=1, *, channel_axis=-1)`
Color difference per CIEDE 2000 standard.

**Parameters:**
- `lab1` array_like: Reference color (Lab colorspace)
- `lab2` array_like: Comparison color (Lab colorspace)
- `kL` float (range), optional: Lightness scale factor, usually 1
- `kC` float (range), optional: Chroma scale factor, usually 1
- `kH` float (range), optional: Hue scale factor, usually 1
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `deltaE` array_like: Distance between `lab1` and `lab2`

**Notes:** CIEDE 2000 is a major revision of CIEDE94; perceptual calibration based on automotive paint on smooth surfaces.

---

### `deltaE_ciede94(lab1, lab2, kH=1, kC=1, kL=1, k1=0.045, k2=0.015, *, channel_axis=-1)`
Color difference per CIEDE 94 standard.

**Parameters:**
- `lab1` array_like: Reference color (Lab colorspace)
- `lab2` array_like: Comparison color (Lab colorspace)
- `kH` float, optional: Hue scale
- `kC` float, optional: Chroma scale
- `kL` float, optional: Lightness scale
- `k1` float, optional: First scale parameter
- `k2` float, optional: Second scale parameter
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `dE` array_like: Color difference between `lab1` and `lab2`

**Notes:** Not symmetric with respect to lab1/lab2; first color regarded as "reference." Parameters depend on application; defaults are for graphic arts. Textile industry uses kL=2.000, k1=0.048, k2=0.014

---

### `deltaE_cmc(lab1, lab2, kL=1, kC=1, *, channel_axis=-1)`
Color difference from CMC l:c standard.

**Parameters:**
- `lab1` array_like: Reference color (Lab colorspace)
- `lab2` array_like: Comparison color (Lab colorspace)
- `kL` float, optional: Lightness weight
- `kC` float, optional: Chroma weight
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `dE` array_like: Distance between colors `lab1` and `lab2`

**Notes:** Developed by Colour Measurement Committee (CMC) for textile industry. Scale factors: kL=2, kC=1 for "acceptability"; kL=1, kC=1 for "imperceptibility." Colors with dE > 1 are "different" for given scales. Not symmetric: `deltaE_cmc(lab1, lab2) != deltaE_cmc(lab2, lab1)`

---

### `gray2rgb(image, *, channel_axis=-1)`
Create RGB representation of gray-level image.

**Parameters:**
- `image` array_like: Input image
- `channel_axis` int, optional: Output axis corresponding to channels

**Returns:**
- `rgb` (…, C=3, …) ndarray: RGB image with new dimension of length 3

**Notes:** 1-D input of shape (M,) produces output shape (M, C=3)

---

### `gray2rgba(image, alpha=None, *, channel_axis=-1)`
Create RGBA representation of gray-level image.

**Parameters:**
- `image` array_like: Input image
- `alpha` array_like, optional: Alpha channel; scalar or broadcastable array. Defaults to maximum value of image dtype
- `channel_axis` int, optional: Output axis corresponding to channels (added in 0.19)

**Returns:**
- `rgba` ndarray: RGBA image with new dimension of length 4 added to input shape

---

### `hed2rgb(hed, *, channel_axis=-1)`
Haematoxylin-Eosin-DAB (HED) to RGB color space conversion.

**Parameters:**
- `hed` (…, C=3, …) array_like: Image in HED color space; final dimension denotes channels by default
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `out` (…, C=3, …) ndarray: Image in RGB, same dimensions as input

**Raises:**
- ValueError: If `hed` not at least 2-D with shape (…, C=3, …)

---

### `hsv2rgb(hsv, *, channel_axis=-1)`
HSV to RGB color space conversion.

**Parameters:**
- `hsv` (…, C=3, …) array_like: Image in HSV format; final dimension denotes channels by default
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `out` (…, C=3, …) ndarray: Image in RGB format, same dimensions as input

**Raises:**
- ValueError: If `hsv` not at least 2-D with shape (…, C=3, …)

**Notes:** Conversion between RGB and HSV color spaces results in some loss of precision, due to integer arithmetic and rounding.

---

### `lab2lch(lab, *, channel_axis=-1)`
Convert CIE-LAB to CIE-LCh color space.

**Parameters:**
- `lab` (…, C=3, …) array_like: Input in CIE-LAB; final dimension denotes channels unless `channel_axis` set. L* ranges 0-100; a*, b* range -128 to 127
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `out` (…, C=3, …) ndarray: Image in CIE-LCh color space, same shape as input

**Raises:**
- ValueError: If `lab` lacks 3 channels (L*, a*, b*)

**Notes:** CIE-LCh is cylindrical representation of CIE-LAB (Cartesian). Hue channel expressed as angle in range (0, 2*pi)

---

### `lab2rgb(lab, illuminant='D65', observer='2', *, channel_axis=-1)`
Convert CIE-LAB to sRGB color space.

**Parameters:**
- `lab` (…, C=3, …) array_like: Input in CIE-LAB; L* ranges 0-100; a*, b* range -128 to 127
- `illuminant` {"A", "B", "C", "D50", "D55", "D65", "D75", "E"}, optional: Illuminant name (case-insensitive)
- `observer` {"2", "10", "R"}, optional: Aperture angle of observer
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `out` (…, C=3, …) ndarray: Image in sRGB color space, same shape as input

**Raises:**
- ValueError: If `lab` not at least 2-D with shape (…, C=3, …)

**Notes:** Uses `lab2xyz()` and `xyz2rgb()`. Default CIE XYZ tristimulus values: x_ref=95.047, y_ref=100, z_ref=108.883

---

### `lab2xyz(lab, illuminant='D65', observer='2', *, channel_axis=-1)`
Convert CIE-LAB to XYZ color space.

**Parameters:**
- `lab` (…, C=3, …) array_like: Input in CIE-LAB; L* ranges 0-100; a*, b* range -128 to 127
- `illuminant` {"A", "B", "C", "D50", "D55", "D65", "D75", "E"}, optional: Illuminant name (case-insensitive)
- `observer` {"2", "10", "R"}, optional: Aperture angle of observer
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `out` (…, C=3, …) ndarray: Image in XYZ color space, same shape as input

**Raises:**
- ValueError: If `lab` not at least 2-D with shape (…, C=3, …); if illuminant/observer unsupported
- UserWarning: If any pixels invalid (Z < 0)

**Notes:** CIE XYZ tristimulus values: x_ref=95.047, y_ref=100, z_ref=108.883

---

### `label2rgb(label, image=None, colors=None, alpha=0.3, bg_label=0, bg_color=(0, 0, 0), image_alpha=1, kind='overlay', *, saturation=0, channel_axis=-1)`
Return RGB image where color-coded labels are painted over image.

**Parameters:**
- `label` ndarray: Integer array of labels with same shape as `image`
- `image` ndarray, optional: Image used as underlay; RGB images converted to grayscale before coloring
- `colors` list, optional: List of colors; cycles if label count exceeds color count
- `alpha` float [0, 1], optional: Opacity of colorized labels (ignored if image is None)
- `bg_label` int, optional: Label treated as background
- `bg_color` str or array, optional: Background color; name in `skimage.color.color_dict` or RGB values [0, 1]
- `image_alpha` float [0, 1], optional: Opacity of image
- `kind` string, {'overlay', 'avg'}: 'overlay' cycles colors overlaying labels; 'avg' replaces segments with average color
- `saturation` float [0, 1], optional: Saturation control; applies only with `kind='overlay'`
- `channel_axis` int, optional: Output axis corresponding to channels (added in 0.19)

**Returns:**
- `result` ndarray of float, same shape as `image`: Blending result of colormap cycling with image at specified alpha

---

### `lch2lab(lch, *, channel_axis=-1)`
Convert CIE-LCh to CIE-LAB color space.

**Parameters:**
- `lch` (…, C=3, …) array_like: Input in CIE-LCh; L* ranges 0-100; C ranges 0-100; h ranges 0 to 2*pi
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `out` (…, C=3, …) ndarray: Image in CIE-LAB format, same shape as input

**Raises:**
- ValueError: If `lch` lacks 3 channels (L*, C, h)

---

### `luv2rgb(luv, *, channel_axis=-1)`
Luv to RGB color space conversion.

**Parameters:**
- `luv` (…, C=3, …) array_like: Image in CIE Luv format; final dimension denotes channels by default
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `out` (…, C=3, …) ndarray: Image in RGB format, same dimensions as input

**Raises:**
- ValueError: If `luv` not at least 2-D with shape (…, C=3, …)

**Notes:** Uses `luv2xyz` and `xyz2rgb`

---

### `luv2xyz(luv, illuminant='D65', observer='2', *, channel_axis=-1)`
CIE-Luv to XYZ color space conversion.

**Parameters:**
- `luv` (…, C=3, …) array_like: Image in CIE-Luv format; final dimension denotes channels by default
- `illuminant` {"A", "B", "C", "D50", "D55", "D65", "D75", "E"}, optional: Illuminant name (case-insensitive)
- `observer` {"2", "10", "R"}, optional: Aperture angle of observer
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `out` (…, C=3, …) ndarray: Image in XYZ format, same dimensions as input

**Raises:**
- ValueError: If `luv` not at least 2-D with shape (…, C=3, …); if illuminant/observer unsupported

**Notes:** Reference whitepoint for D65 Illuminant with tristimulus values (95.047, 100., 108.883)

---

### `rgb2gray(rgb, *, channel_axis=-1)`
Compute luminance of RGB image.

**Parameters:**
- `rgb` (…, C=3, …) array_like: Image in RGB format; final dimension denotes channels by default

**Returns:**
- `out` ndarray: Luminance image, same size as input but with channel dimension removed

**Raises:**
- ValueError: If `rgb` not at least 2-D with shape (…, C=3, …)

**Notes:** Weights used in this conversion are calibrated for contemporary CRT phosphors: Y = 0.2125 R + 0.7154 G + 0.0721 B. Alpha channel ignored if present.

---

### `rgb2hed(rgb, *, channel_axis=-1)`
RGB to Haematoxylin-Eosin-DAB (HED) color space conversion.

**Parameters:**
- `rgb` (…, C=3, …) array_like: Image in RGB format; final dimension denotes channels by default
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `out` (…, C=3, …) ndarray: Image in HED format, same dimensions as input

**Raises:**
- ValueError: If `rgb` not at least 2-D with shape (…, C=3, …)

---

### `rgb2hsv(rgb, *, channel_axis=-1)`
RGB to HSV color space conversion.

**Parameters:**
- `rgb` (…, C=3, …) array_like: Image in RGB format; final dimension denotes channels by default
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `out` (…, C=3, …) ndarray: Image in HSV format, same dimensions as input

**Raises:**
- ValueError: If `rgb` not at least 2-D with shape (…, C=3, …)

**Notes:** Conversion between RGB and HSV color spaces results in some loss of precision, due to integer arithmetic and rounding.

---

### `rgb2lab(rgb, illuminant='D65', observer='2', *, channel_axis=-1)`
Conversion from sRGB (IEC 61966-2-1:1999) to CIE Lab colorspace.

**Parameters:**
- `rgb` (…, C=3, …) array_like: Image in RGB format; final dimension denotes channels by default
- `illuminant` {"A", "B", "C", "D50", "D55", "D65", "D75", "E"}, optional: Illuminant name (case-insensitive)
- `observer` {"2", "10", "R"}, optional: Aperture angle of observer
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `out` (…, C=3, …) ndarray: Image in Lab format, same dimensions as input

**Raises:**
- ValueError: If `rgb` not at least 2-D with shape (…, C=3, …)

**Notes:** RGB is device-dependent; ensure image mapped to sRGB color space. Uses `rgb2xyz` and `xyz2lab`. Default: Observer="2", Illuminant="D65". CIE XYZ tristimulus values x_ref=95.047, y_ref=100, z_ref=108.883

---

### `rgb2luv(rgb, *, channel_axis=-1)`
RGB to CIE-Luv color space conversion.

**Parameters:**
- `rgb` (…, C=3, …) array_like: Image in RGB format; final dimension denotes channels by default
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `out` (…, C=3, …) ndarray: Image in CIE Luv format, same dimensions as input

**Raises:**
- ValueError: If `rgb` not at least 2-D with shape (…, C=3, …)

---

### `rgb2rgbcie(rgb, *, channel_axis=-1)`
RGB to RGB CIE color space conversion.

**Parameters:**
- `rgb` (…, C=3, …) array_like: Image in RGB format; final dimension denotes channels by default
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `out` (…, C=3, …) ndarray: Image in RGB CIE format, same dimensions as input

**Raises:**
- ValueError: If `rgb` not at least 2-D with shape (…, C=3, …)

---

### `rgb2xyz(rgb, *, channel_axis=-1)`
RGB to XYZ color space conversion.

**Parameters:**
- `rgb` (…, C=3, …) array_like: Image in RGB format; final dimension denotes channels by default
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `out` (…, C=3, …) ndarray: Image in XYZ format, same dimensions as input

**Raises:**
- ValueError: If `rgb` not at least 2-D with shape (…, C=3, …)

**Notes:** CIE XYZ derived from CIE RGB; however this function converts from sRGB.

---

### `rgb2ycbcr(rgb, *, channel_axis=-1)`
RGB to YCbCr color space conversion.

**Parameters:**
- `rgb` (…, C=3, …) array_like: Image in RGB format; final dimension denotes channels by default
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `out` (…, C=3, …) ndarray: Image in YCbCr format, same dimensions as input

**Raises:**
- ValueError: If `rgb` not at least 2-D with shape (…, C=3, …)

**Notes:** Y between 16 and 235; commonly used by video codecs, sometimes incorrectly called "YUV"

---

### `rgb2ydbdr(rgb, *, channel_axis=-1)`
RGB to YDbDr color space conversion.

**Parameters:**
- `rgb` (…, C=3, …) array_like: Image in RGB format; final dimension denotes channels by default
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `out` (…, C=3, …) ndarray: Image in YDbDr format, same dimensions as input

**Raises:**
- ValueError: If `rgb` not at least 2-D with shape (…, C=3, …)

**Notes:** Commonly used by video codecs; reversible color transform in JPEG2000

---

### `rgb2yiq(rgb, *, channel_axis=-1)`
RGB to YIQ color space conversion.

**Parameters:**
- `rgb` (…, C=3, …) array_like: Image in RGB format; final dimension denotes channels by default
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `out` (…, C=3, …) ndarray: Image in YIQ format, same dimensions as input

**Raises:**
- ValueError: If `rgb` not at least 2-D with shape (…, C=3, …)

---

### `rgb2ypbpr(rgb, *, channel_axis=-1)`
RGB to YPbPr color space conversion.

**Parameters:**
- `rgb` (…, C=3, …) array_like: Image in RGB format; final dimension denotes channels by default
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `out` (…, C=3, …) ndarray: Image in YPbPr format, same dimensions as input

**Raises:**
- ValueError: If `rgb` not at least 2-D with shape (…, C=3, …)

---

### `rgb2yuv(rgb, *, channel_axis=-1)`
RGB to YUV color space conversion.

**Parameters:**
- `rgb` (…, C=3, …) array_like: Image in RGB format; final dimension denotes channels by default
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `out` (…, C=3, …) ndarray: Image in YUV format, same dimensions as input

**Raises:**
- ValueError: If `rgb` not at least 2-D with shape (…, C=3, …)

**Notes:** Y between 0 and 1; use YCbCr for video codecs where Y ranges 16-235

---

### `rgba2rgb(rgba, background=(1, 1, 1), *, channel_axis=-1)`
RGBA to RGB conversion using alpha blending.

**Parameters:**
- `rgba` (…, C=4, …) array_like: Image in RGBA format; final dimension denotes channels by default
- `background` array_like: Background color for blending (3 floats between 0-1, RGB values)
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `out` (…, C=3, …) ndarray: Image in RGB format, same dimensions as input

**Raises:**
- ValueError: If `rgba` not at least 2D with shape (…, 4, …)

---

### `rgbcie2rgb(rgbcie, *, channel_axis=-1)`
RGB CIE to RGB color space conversion.

**Parameters:**
- `rgbcie` (…, C=3, …) array_like: Image in RGB CIE format; final dimension denotes channels by default
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `out` (…, C=3, …) ndarray: Image in RGB format, same dimensions as input

**Raises:**
- ValueError: If `rgbcie` not at least 2-D with shape (…, C=3, …)

---

### `separate_stains(rgb, conv_matrix, *, channel_axis=-1)`
RGB to stain color space conversion.

**Parameters:**
- `rgb` (…, C=3, …) array_like: Image in RGB format; final dimension denotes channels by default
- `conv_matrix` ndarray: Stain separation matrix as described by G. Landini
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `out` (…, C=3, …) ndarray: Image in stain color space, same dimensions as input

**Raises:**
- ValueError: If `rgb` not at least 2-D with shape (…, C=3, …)

**Notes:** Available stain separation matrices: `hed_from_rgb`, `hdx_from_rgb`, `fgx_from_rgb`, `bex_from_rgb`, `rbd_from_rgb`, `gdx_from_rgb`, `hax_from_rgb`, `bro_from_rgb`, `bpx_from_rgb`, `ahx_from_rgb`, `hpx_from_rgb`. Implementation borrows from DIPlib; compensation using small value avoids log artifacts in Beer-Lambert law calculation.

---

### `xyz2lab(xyz, illuminant='D65', observer='2', *, channel_axis=-1)`
XYZ to CIE-LAB color space conversion.

**Parameters:**
- `xyz` (…, C=3, …) array_like: Image in XYZ format; final dimension denotes channels by default
- `illuminant` {"A", "B", "C", "D50", "D55", "D65", "D75", "E"}, optional: Illuminant name (case-insensitive)
- `observer` {"2", "10", "R"}, optional: Aperture angle of observer or 'R' for R function compatibility
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `out` (…, C=3, …) ndarray: Image in CIE-LAB format, same dimensions as input

**Raises:**
- ValueError: If `xyz` not at least 2-D with shape (…, C=3, …); if illuminant/observer unsupported

**Notes:** Default Observer="2", Illuminant="D65". CIE XYZ tristimulus values x_ref=95.047, y_ref=100, z_ref=108.883

---

### `xyz2luv(xyz, illuminant='D65', observer='2', *, channel_axis=-1)`
XYZ to CIE-Luv color space conversion.

**Parameters:**
- `xyz` (…, C=3, …) array_like: Image in XYZ format; final dimension denotes channels by default
- `illuminant` {"A", "B", "C", "D50", "D55", "D65", "D75", "E"}, optional: Illuminant name (case-insensitive)
- `observer` {"2", "10", "R"}, optional: Aperture angle of observer
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `out` (…, C=3, …) ndarray: Image in CIE-Luv format, same dimensions as input

**Raises:**
- ValueError: If `xyz` not at least 2-D with shape (…, C=3, …); if illuminant/observer unsupported

**Notes:** Reference whitepoint for D65 with tristimulus values (95.047, 100., 108.883)

---

### `xyz2rgb(xyz, *, channel_axis=-1)`
XYZ to RGB color space conversion.

**Parameters:**
- `xyz` (…, C=3, …) array_like: Image in XYZ format; final dimension denotes channels by default
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `out` (…, C=3, …) ndarray: Image in RGB format, same dimensions as input

**Raises:**
- ValueError: If `xyz` not at least 2-D with shape (…, C=3, …)

**Notes:** CIE XYZ derived from CIE RGB; however this function converts to sRGB.

---

### `xyz_tristimulus_values(*, illuminant, observer, dtype=<class 'float'>)`
Get CIE XYZ tristimulus values.

**Parameters:**
- `illuminant` {"A", "B", "C", "D50", "D55", "D65", "D75", "E"}: Illuminant name (case-insensitive)
- `observer` {"2", "10", "R"}: 2-degree observer, 10-degree observer, or 'R' for R function compatibility
- `dtype` dtype, optional: Output data type

**Returns:**
- `values` array: Array with 3 elements (X, Y, Z) containing CIE XYZ tristimulus values scaled so Y=1

**Raises:**
- ValueError: If illuminant/observer unsupported

---

### `ycbcr2rgb(ycbcr, *, channel_axis=-1)`
YCbCr to RGB color space conversion.

**Parameters:**
- `ycbcr` (…, C=3, …) array_like: Image in YCbCr format; final dimension denotes channels by default
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `out` (…, C=3, …) ndarray: Image in RGB format, same dimensions as input

**Raises:**
- ValueError: If `ycbcr` not at least 2-D with shape (…, C=3, …)

**Notes:** Y between 16 and 235; commonly used by video codecs, sometimes incorrectly called "YUV"

---

### `ydbdr2rgb(ydbdr, *, channel_axis=-1)`
YDbDr to RGB color space conversion.

**Parameters:**
- `ydbdr` (…, C=3, …) array_like: Image in YDbDr format; final dimension denotes channels by default
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `out` (…, C=3, …) ndarray: Image in RGB format, same dimensions as input

**Raises:**
- ValueError: If `ydbdr` not at least 2-D with shape (…, C=3, …)

---

### `yiq2rgb(yiq, *, channel_axis=-1)`
YIQ to RGB color space conversion.

**Parameters:**
- `yiq` (…, C=3, …) array_like: Image in YIQ format; final dimension denotes channels by default
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `out` (…, C=3, …) ndarray: Image in RGB format, same dimensions as input

**Raises:**
- ValueError: If `yiq` not at least 2-D with shape (…, C=3, …)

---

### `ypbpr2rgb(ypbpr, *, channel_axis=-1)`
YPbPr to RGB color space conversion.

**Parameters:**
- `ypbpr` (…, C=3, …) array_like: Image in YPbPr format; final dimension denotes channels by default
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `out` (…, C=3, …) ndarray: Image in RGB format, same dimensions as input

**Raises:**
- ValueError: If `ypbpr` not at least 2-D with shape (…, C=3, …)

---

### `yuv2rgb(yuv, *, channel_axis=-1)`
YUV to RGB color space conversion.

**Parameters:**
- `yuv` (…, C=3, …) array_like: Image in YUV format; final dimension denotes channels by default
- `channel_axis` int, optional: Axis corresponding to channels (added in 0.19)

**Returns:**
- `out` (…, C=3, …) ndarray: Image in RGB format, same dimensions as input

**Raises:**
- ValueError: If `yuv` not at least 2-D with shape (…, C=3, …)
