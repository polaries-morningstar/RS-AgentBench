# Rasterio: Geospatial Raster I/O

Source: https://rasterio.readthedocs.io/en/stable/quickstart.html
Source: https://rasterio.readthedocs.io/en/stable/topics/reading.html
Source: https://rasterio.readthedocs.io/en/stable/topics/writing.html
Source: https://rasterio.readthedocs.io/en/stable/topics/reproject.html
Source: https://rasterio.readthedocs.io/en/stable/api/rasterio.crs.html

Reading and writing data files is a spatial data programmer's bread and butter. This document explains how to use Rasterio to read existing files and to create new files. Some advanced topics are glossed over to be covered in more detail elsewhere in Rasterio's documentation. Only the GeoTIFF format is used here, but the examples do apply to other raster data formats. It is presumed that Rasterio has been installed.

---

## Source: https://rasterio.readthedocs.io/en/stable/quickstart.html

# Python Quickstart

## Opening a dataset in reading mode

Consider a GeoTIFF file named `example.tif` with 16-bit Landsat 8 imagery covering a part of the United States's Colorado Plateau. Because the imagery is large (70 MB) and has a wide dynamic range it is difficult to display it in a browser. A rescaled and dynamically squashed version is shown below.

Import rasterio to begin.

```
>>> import rasterio
```

Next, open the file.

```
>>> dataset = rasterio.open('example.tif')
```

Rasterio's open() function takes a path string or path-like object and returns an opened dataset object. The path may point to a file of any supported raster format. Rasterio will open it using the proper GDAL format driver. Dataset objects have some of the same attributes as Python file objects.

```
>>> dataset.name
'example.tif'
>>> dataset.mode
'r'
>>> dataset.closed
False
```

## Dataset attributes

Properties of the raster data stored in the example GeoTIFF can be accessed through attributes of the opened dataset object. Dataset objects have bands and this example has a band count of 1.

```
>>> dataset.count
1
```

A dataset band is an array of values representing the partial distribution of a single variable in 2-dimensional (2D) space. All band arrays of a dataset have the same number of rows and columns. The variable represented by the example dataset's sole band is Level-1 digital numbers (DN) for the Landsat 8 Operational Land Imager (OLI) band 4 (wavelengths between 640-670 nanometers). These values can be scaled to radiance or reflectance values. The array of DN values is 7731 columns wide and 7871 rows high.

```
>>> dataset.width
7731
>>> dataset.height
7871
```

Some dataset attributes expose the properties of all dataset bands via a tuple of values, one per band. To get a mapping of band indexes to variable data types, apply a dictionary comprehension to the zip() product of a dataset's DatasetReader.indexes and DatasetReader.dtypes attributes.

```
>>> {i: dtype for i, dtype in zip(dataset.indexes, dataset.dtypes)}
{1: 'uint16'}
```

The example file's sole band contains unsigned 16-bit integer values. The GeoTIFF format also supports signed integers and floats of different size.

## Dataset georeferencing

A GIS raster dataset is different from an ordinary image; its elements (or "pixels") are mapped to regions on the earth's surface. Every pixels of a dataset is contained within a spatial bounding box.

```
>>> dataset.bounds
BoundingBox(left=358485.0, bottom=4028985.0, right=590415.0, top=4265115.0)
```

Our example covers the world from 358485 meters (in this case) to 590415 meters, left to right, and 4028985 meters to 4265115 meters bottom to top. It covers a region 231.93 kilometers wide by 236.13 kilometers high.

The value of DatasetReader.bounds attribute is derived from a more fundamental attribute: the dataset's geospatial transform.

```
>>> dataset.transform
Affine(30.0, 0.0, 358485.0,
       0.0, -30.0, 4265115.0)
```

A dataset's DatasetReader.transform is an affine transformation matrix that maps pixel locations in (col, row) coordinates to (x, y) spatial positions. The product of this matrix and `(0, 0)`, the column and row coordinates of the upper left corner of the dataset, is the spatial position of the upper left corner.

```
>>> dataset.transform * (0, 0)
(358485.0, 4265115.0)
```

The position of the lower right corner is obtained similarly.

```
>>> dataset.transform * (dataset.width, dataset.height)
(590415.0, 4028985.0)
```

But what do these numbers mean? 4028985 meters from where? These coordinate values are relative to the origin of the dataset's coordinate reference system (CRS).

```
>>> dataset.crs
CRS.from_epsg(32612)
```

EPSG:32612 identifies a particular coordinate reference system: UTM zone 12N. This system is used for mapping areas in the Northern Hemisphere between 108 and 114 degrees west. The upper left corner of the example dataset,`(358485.0, 4265115.0)`, is 141.5 kilometers west of zone 12's central meridian (111 degrees west) and 4265 kilometers north of the equator.

Between the DatasetReader.crs and DatasetReader.transform attributes, the georeferencing of a raster dataset is described and the dataset can compared to other GIS datasets.

## Reading raster data

Data from a raster band can be accessed by the band's index number. Following the GDAL convention, bands are indexed from 1.

```
>>> dataset.indexes
(1,)
>>> band1 = dataset.read(1)
```

The DatasetReader.read() method returns a numpy array.

```
>>> band1
array([[0, 0, 0, ..., 0, 0, 0],
       [0, 0, 0, ..., 0, 0, 0],
       [0, 0, 0, ..., 0, 0, 0],
       ...,
       [0, 0, 0, ..., 0, 0, 0],
       [0, 0, 0, ..., 0, 0, 0],
       [0, 0, 0, ..., 0, 0, 0]], dtype=uint16)
```

Values from the array can be addressed by their row, column index.

```
>>> band1[dataset.height // 2, dataset.width // 2]
17491
```

## Spatial indexing

Datasets have an DatasetReader.index() method for getting the array indices corresponding to points in georeferenced space. To get the value for the pixel 100 kilometers east and 50 kilometers south of the dataset's upper left corner, do the following.

```
>>> x, y = (dataset.bounds.left + 100000, dataset.bounds.top - 50000)
>>> row, col = dataset.index(x, y)
>>> row, col
(1666, 3333)
>>> band1[row, col]
7566
```

To get the spatial coordinates of a pixel, use the dataset's DatasetReader.xy() method. The coordinates of the center of the image can be computed like this.

```
>>> dataset.xy(dataset.height // 2, dataset.width // 2)
(476550.0, 4149150.0)
```

## Creating data

Reading data is only half the story. Using Rasterio dataset objects, arrays of values can be written to a raster data file and thus shared with other GIS applications such as QGIS.

As an example, consider an array of floating point values representing, e.g., a temperature or pressure anomaly field measured or modeled on a regular grid, 240 columns by 180 rows. The first and last grid points on the horizontal axis are located at 4.0 degrees west and 4.0 degrees east longitude, the first and last grid points on the vertical axis are located at 3 degrees south and 3 degrees north latitude.

```
>>> import numpy as np
>>> x = np.linspace(-4.0, 4.0, 240)
>>> y = np.linspace(-3.0, 3.0, 180)[::-1]
>>> X, Y = np.meshgrid(x, y)
>>> Z1 = np.exp(-2 * np.log(2) * ((X - 0.5) ** 2 + (Y - 0.5) ** 2) / 1 ** 2)
>>> Z2 = np.exp(-3 * np.log(2) * ((X + 0.5) ** 2 + (Y + 0.5) ** 2) / 2.5 ** 2)
>>> Z = 10.0 * (Z2 - Z1)
```

The fictional field for this example consists of the difference of two Gaussian distributions and is represented by the array `Z`. Its contours are shown below.

## Opening a dataset in writing mode

To save this array along with georeferencing information to a new raster data file, call rasterio.open() with a path to the new file to be created,`'w'` to specify writing mode, and several keyword arguments.

* driver: the name of the desired format driver
* width: the number of columns of the dataset
* height: the number of rows of the dataset
* count: a count of the dataset bands
* dtype: the data type of the dataset
* crs: a coordinate reference system identifier or description
* transform: an affine transformation matrix, and
* nodata: a "nodata" value

The first 5 of these keyword arguments parametrize fixed, format-specific properties of the data file and are required when opening a file to write. The last 3 are optional.

In this example the coordinate reference system will be `'+proj=latlong'`, which describes an equirectangular coordinate reference system with units of decimal degrees. The proper affine transformation matrix can be computed from the matrix product of a translation and a scaling.

```
>>> from rasterio.transform import Affine
>>> res = (x[-1] - x[0]) / 240.0
>>> transform = Affine.translation(x[0] - res / 2, y[0] + res / 2) * Affine.scale(res, -res)
>>> transform
Affine(0.03333333333333333, 0.0, -4.016666666666667,
       0.0, -0.03333333333333333, 3.0166666666666666)
```

The upper left point in the example grid is at 3 degrees west and 2 degrees north. The raster pixel centered on this grid point extends `res / 2`, or 1/60 degrees, in each direction, hence the shift in the expression above.

A dataset for storing the example grid is opened like so

```
>>> new_dataset = rasterio.open(
...     '/tmp/new.tif',
...     'w',
...     driver='GTiff',
...     height=Z.shape[0],
...     width=Z.shape[1],
...     count=1,
...     dtype=Z.dtype,
...     crs='+proj=latlong',
...     transform=transform,
... )
```

Values for the height, width, and dtype keyword arguments are taken directly from attributes of the 2-D array, `Z`. Not all raster formats can support the 64-bit float values in `Z`, but the GeoTIFF format can.

## Saving raster data

To copy the grid to the opened dataset, call the new dataset's DatasetWriter.write() method with the grid and target band number as arguments.

```
>>> new_dataset.write(Z, 1)
```

Then call the DatasetWriter.close() method to sync data to disk and finish.

```
>>> new_dataset.close()
```

Because Rasterio's dataset objects mimic Python's file objects and implement Python's context manager protocol, it is possible to do the following instead.

```
with rasterio.open(
    '/tmp/new.tif',
    'w',
    driver='GTiff',
    height=Z.shape[0],
    width=Z.shape[1],
    count=1,
    dtype=Z.dtype,
    crs='+proj=latlong',
    transform=transform,
) as dst:
    dst.write(Z, 1)
```

These are the basics of reading and writing raster data files. More features and examples are contained in the advanced topics section.

---

## Source: https://rasterio.readthedocs.io/en/stable/topics/reading.html

# Reading Datasets

Dataset objects provide read, read-write, and write access to raster data files and are obtained by calling rasterio.open(). That function mimics Python's built-in open() and the dataset objects it returns mimic Python file objects.

```
>>> import rasterio
>>> src = rasterio.open('tests/data/RGB.byte.tif')
>>> src
<open DatasetReader name='tests/data/RGB.byte.tif' mode='r'>
>>> src.name
'tests/data/RGB.byte.tif'
>>> src.mode
'r'
>>> src.closed
False
```

If you try to access a nonexistent path, rasterio.open() does the same thing as open(), raising an exception immediately.

```
>>> open('/lol/wut.tif')
Traceback (most recent call last):
 ...
FileNotFoundError: [Errno 2] No such file or directory: '/lol/wut.tif'
>>> rasterio.open('/lol/wut.tif')
Traceback (most recent call last):
 ...
rasterio.errors.RasterioIOError: No such file or directory
```

Datasets generally have one or more bands (or layers). Following the GDAL convention, these are indexed starting with the number 1. The first band of a file can be read like this:

```
>>> array = src.read(1)
>>> array.shape
(718, 791)
```

The returned object is a 2-dimensional numpy.ndarray. The representation of that array at the Python prompt is a summary; the GeoTIFF file that Rasterio uses for testing has 0 values in the corners, but has nonzero values elsewhere.

```
>>> from matplotlib import pyplot
>>> pyplot.imshow(array, cmap='pink')
<matplotlib.image.AxesImage object at 0x...>
>>> pyplot.show()
```

Instead of reading single bands, all bands of the input dataset can be read into a 3-dimensonal ndarray. Note that the interpretation of the 3 axes is `(bands, rows, columns)`.

```
>>> array = src.read()
>>> array.shape
(3, 718, 791)
```

In order to read smaller chunks of the dataset, refer to documentation on windowed reading and writing.

The indexes, Numpy data types, and nodata values of all a dataset's bands can be had from its indexes, dtypes, and nodatavals attributes.

```
>>> for i, dtype, nodataval in zip(src.indexes, src.dtypes, src.nodatavals):
...     print(i, dtype, nodataval)
...
1 uint8 0.0
2 uint8 0.0
3 uint8 0.0
```

To close a dataset, call its close() method.

```
>>> src.close()
>>> src
<closed DatasetReader name='tests/data/RGB.byte.tif' mode='r'>
```

After it's closed, data can no longer be read.

```
>>> src.read(1)
Traceback (most recent call last):
 ...
ValueError: can't read closed raster file
```

This is the same behavior as Python's file.

```
>>> f = open('README.rst')
>>> f.close()
>>> f.read()
Traceback (most recent call last):
 ...
ValueError: I/O operation on closed file.
```

As Python file objects can, Rasterio datasets can manage the entry into and exit from runtime contexts created using a `with` statement. This ensures that files are closed no matter what exceptions may be raised within the the block.

```
>>> with rasterio.open('tests/data/RGB.byte.tif', 'r') as one:
...     with rasterio.open('tests/data/RGB.byte.tif', 'r') as two:
...         print(two)
...     print(one)
...     raise Exception("an error occurred")
...
<open DatasetReader name='tests/data/RGB.byte.tif' mode='r'>
<open DatasetReader name='tests/data/RGB.byte.tif' mode='r'>
Traceback (most recent call last):
  File "<stdin>", line 5, in <module>
Exception: an error occurred
>>> print(two)
<closed DatasetReader name='tests/data/RGB.byte.tif' mode='r'>
>>> print(one)
<closed DatasetReader name='tests/data/RGB.byte.tif' mode='r'>
```

Format-specific dataset reading options may be passed as keyword arguments. For example, to turn off all types of GeoTIFF georeference except that within the TIFF file's keys and tags, pass GEOREF_SOURCES='INTERNAL'.

```
>>> with rasterio.open('tests/data/RGB.byte.tif', GEOREF_SOURCES='INTERNAL') as dataset:
...     # .aux.xml, .tab, .tfw sidecar files will be ignored.
```

---

## Source: https://rasterio.readthedocs.io/en/stable/topics/writing.html

# Writing Datasets

Todo

* appending to existing data
* context manager
* write 3d vs write 2d
* document issues with writing compressed files (per #77)
* discuss and refer to topics
   * creation options
   * transforms
   * dtypes
   * block windows

Opening a file in writing mode is a little more complicated than opening a text file in Python. The dimensions of the raster dataset, the data types, and the specific format must be specified.

Here's an example of basic rasterio functionality. An array is written to a new single band TIFF.

```python
# Register GDAL format drivers and configuration options with a
# context manager.
with rasterio.Env():

    # Write an array as a raster band to a new 8-bit file. For
    # the new file's profile, we start with the profile of the source
    profile = src.profile

    # And then change the band count to 1, set the
    # dtype to uint8, and specify LZW compression.
    profile.update(
        dtype=rasterio.uint8,
        count=1,
        compress='lzw')

    with rasterio.open('example.tif', 'w', **profile) as dst:
        dst.write(array.astype(rasterio.uint8), 1)

# At the end of the ``with rasterio.Env()`` block, context
# manager exits and all drivers are de-registered.
```

Writing data mostly works as with a Python file. There are a few format-specific differences.

## Supported Drivers

`GTiff` is the only driver that supports writing directly to disk. GeoTiffs use the `RasterUpdater` and leverage the full capabilities of the GDALCreate() function. We highly recommend using GeoTiff driver for writing as it is the best-tested and best-supported format.

Some other formats that are writable by GDAL can also be written by Rasterio. These use an `IndirectRasterUpdater` which does not create directly but uses a temporary in-memory dataset and GDALCreateCopy() to produce the final output.

Some formats are known to produce invalid results using the `IndirectRasterUpdater`. These formats will raise a RasterioIOError if you attempt to write to them. Currently this applies to the `netCDF` driver but users are encouraged to report problems with other formats.

---

## Source: https://rasterio.readthedocs.io/en/stable/topics/reproject.html

# Reprojection

Rasterio can map the pixels of a destination raster with an associated coordinate reference system and transform to the pixels of a source image with a different coordinate reference system and transform. This process is known as reprojection.

Rasterio's `rasterio.warp.reproject()` is a geospatial-specific analog to SciPy's `scipy.ndimage.interpolation.geometric_transform()` [1].

The code below reprojects between two arrays, using no pre-existing GIS datasets. `rasterio.warp.reproject()` has two positional arguments: source and destination. The remaining keyword arguments parameterize the reprojection transform.

```python
import numpy as np
import rasterio
from rasterio import Affine as A
from rasterio.warp import reproject, Resampling

with rasterio.Env():

    # As source: a 512 x 512 raster centered on 0 degrees E and 0
    # degrees N, each pixel covering 15".
    rows, cols = src_shape = (512, 512)
    d = 1.0/240 # decimal degrees per pixel
    # The following is equivalent to
    # A(d, 0, -cols*d/2, 0, -d, rows*d/2).
    src_transform = A.translation(-cols*d/2, rows*d/2) * A.scale(d, -d)
    src_crs = {'init': 'EPSG:4326'}
    source = np.ones(src_shape, np.uint8)*255

    # Destination: a 1024 x 1024 dataset in Web Mercator (EPSG:3857)
    # with origin at 0.0, 0.0.
    dst_shape = (1024, 1024)
    dst_transform = A.translation(-237481.5, 237536.4) * A.scale(425.0, -425.0)
    dst_crs = {'init': 'EPSG:3857'}
    destination = np.zeros(dst_shape, np.uint8)

    reproject(
        source,
        destination,
        src_transform=src_transform,
        src_crs=src_crs,
        dst_transform=dst_transform,
        dst_crs=dst_crs,
        resampling=Resampling.nearest)

    # Assert that the destination is only partly filled.
    assert destination.any()
    assert not destination.all()
```

See `examples/reproject.py` for code that writes the destination array to a GeoTIFF file.

## Estimating optimal output shape

Rasterio provides a `rasterio.warp.calculate_default_transform()` function to determine the optimal resolution and transform for the destination raster. Given a source dataset in a known coordinate reference system, this function will return a `transform, width, height` tuple which is calculated by libgdal.

## Reprojecting a GeoTIFF dataset

Reprojecting a GeoTIFF dataset from one coordinate reference system is a common use case. Rasterio provides a few utilities to make this even easier:

`transform_bounds()` transforms the bounding coordinates of the source raster to the target coordinate reference system, densifiying points along the edges to account for non-linear transformations of the edges.

`calculate_default_transform()` transforms bounds to target coordinate system, calculates resolution if not provided, and returns destination transform and dimensions.

```python
import numpy as np
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

dst_crs = 'EPSG:4326'

with rasterio.open('rasterio/tests/data/RGB.byte.tif') as src:
    transform, width, height = calculate_default_transform(
        src.crs, dst_crs, src.width, src.height, *src.bounds)
    kwargs = src.meta.copy()
    kwargs.update({
        'crs': dst_crs,
        'transform': transform,
        'width': width,
        'height': height
    })

    with rasterio.open('/tmp/RGB.byte.wgs84.tif', 'w', **kwargs) as dst:
        for i in range(1, src.count + 1):
            reproject(
                source=rasterio.band(src, i),
                destination=rasterio.band(dst, i),
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs=dst_crs,
                resampling=Resampling.nearest)
```

See `rasterio/rio/warp.py` for more complex examples of reprojection based on new bounds, dimensions, and resolution (as well as a command-line interface described here).

It is also possible to use `reproject()` to create an output dataset zoomed out by a factor of 2. Methods of the `rasterio.Affine` class help us generate the output dataset's transform matrix and, thereby, its spatial extent.

```python
import numpy as np
import rasterio
from rasterio import Affine as A
from rasterio.warp import reproject, Resampling

with rasterio.open('rasterio/tests/data/RGB.byte.tif') as src:
    src_transform = src.transform

    # Zoom out by a factor of 2 from the center of the source
    # dataset. The destination transform is the product of the
    # source transform, a translation down and to the right, and
    # a scaling.
    dst_transform = src_transform*A.translation(
        -src.width/2.0, -src.height/2.0)*A.scale(2.0)

    data = src.read()

    kwargs = src.meta
    kwargs['transform'] = dst_transform

    with rasterio.open('/tmp/zoomed-out.tif', 'w', **kwargs) as dst:

        for i, band in enumerate(data, 1):
            dest = np.zeros_like(band)

            reproject(
                band,
                dest,
                src_transform=src_transform,
                src_crs=src.crs,
                dst_transform=dst_transform,
                dst_crs=src.crs,
                resampling=Resampling.nearest)

            dst.write(dest, indexes=i)
```

## Reprojecting with other georeferencing metadata

Most geospatial datasets have a geotransform which can be used to reproject a dataset from one coordinate reference system to another. Datasets may also be georeferenced by alternative metadata, namely Ground Control Points (gcps) or Rational Polynomial Coefficients (rpcs). For details on gcps and rpcs, see Georeferencing. A common scenario is using gcps or rpcs to geocode (orthorectify) datasets, resampling and reorienting them to a coordinate reference system with a newly computed geotransform.

```python
import numpy as np
import rasterio
from rasterio.warp import reproject
from rasterio.enums import Resampling

with rasterio.open('RGB.byte.rpc.vrt') as source:
    print(source.rpcs)
    src_crs = "EPSG:4326"  # This is the crs of the rpcs

    # Optional keyword arguments to be passed to GDAL transformer
    # https://gdal.org/api/gdal_alg.html?highlight=gdalcreategenimgprojtransformer2#_CPPv432GDALCreateGenImgProjTransformer212GDALDatasetH12GDALDatasetHPPc
    kwargs = {
        'RPC_DEM': '/path/to/dem.tif'
    }

    # Destination: a 1024 x 1024 dataset in Web Mercator (EPSG:3857)
    destination = np.zeros((1024, 1024), dtype=np.uint8)
    dst_crs = "EPSG:3857"

    _, dst_transform = reproject(
        rasterio.band(source, 1),
        destination,
        rpcs=source.rpcs,
        src_crs=src_crs,
        dst_crs=dst_crs,
        resampling=Resampling.nearest,
        **kwargs
    )

    assert destination.any()
```

**Note**

When reprojecting a dataset with gcps or rpcs, the `src_crs` parameter should be supplied with the coordinate reference system that the gcps or rpcs are referenced against. By definition rpcs are always referenced against WGS84 ellipsoid with geographic coordinates (EPSG:4326) [2].

## References

[1] https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.geometric_transform.html#scipy.ndimage.geometric_transform

[2] http://geotiff.maptools.org/rpc_prop.html

---

## Source: https://rasterio.readthedocs.io/en/stable/api/rasterio.crs.html

# rasterio.crs module

Coordinate reference systems, the CRS class and supporting functions.

A coordinate reference system (CRS) defines how a dataset's pixels map to locations on, for example, a globe or the Earth. A CRS may be local or global. The GIS field shares a number of authority files that define CRS. "EPSG:32618" is the name of a regional CRS from the European Petroleum Survey Group authority file. "OGC:CRS84" is the name of a global CRS from the Open Geospatial Consortium authority. Custom CRS can be described in text using several formats. Rasterio's CRS class is our abstraction for coordinate reference systems.

A rasterio dataset's crs property is an instance of CRS. CRS are also used to define transformations between coordinate reference systems. These transformations are performed by the PROJ library. Rasterio does not call PROJ functions directly, but invokes them via calls to GDAL's "OSR*" functions.

## class rasterio.crs.CRS(initialdata=None, **kwargs)

A geographic or projected coordinate reference system.

CRS objects may be created by passing PROJ parameters as keyword arguments to the standard constructor or by passing EPSG codes, PROJ mappings, PROJ strings, or WKT strings to the from_epsg, from_dict, from_string, or from_wkt static methods.

### Examples

The from_dict method takes PROJ parameters as keyword arguments.

```python
>>> crs = CRS.from_dict(proj="aea")
```

EPSG codes may be used with the from_epsg method.

```python
>>> crs = CRS.from_epsg(3005)
```

The from_string method takes a variety of input.

```python
>>> crs = CRS.from_string("EPSG:3005")
```

**data**
A PROJ4 dict representation of the CRS.

**static from_authority(auth_name, code)**
Make a CRS from an authority name and code.

Parameters:
- auth_name (str)
- code (int or str) - The code used by the authority.

Return type: CRS

Raises: CRSError

**static from_dict(initialdata=None, **kwargs)**
Make a CRS from a dict of PROJ parameters or PROJ JSON.

Parameters:
- initialdata (mapping, optional) - A dictionary or other mapping
- kwargs (mapping, optional) - Another mapping. Will be overlaid on the initialdata.

Return type: CRS

Raises: CRSError

**static from_epsg(code)**
Make a CRS from an EPSG code.

Parameters:
- code (int or str) - An EPSG code. Strings will be converted to integers.

Notes: The input code is not validated against an EPSG database.

Return type: CRS

Raises: CRSError

**static from_proj4(proj)**
Make a CRS from a PROJ4 string.

Parameters:
- proj (str) - A PROJ4 string like "+proj=longlat …"

Return type: CRS

Raises: CRSError

**static from_string(value, morph_from_esri_dialect=False)**
Make a CRS from an EPSG, PROJ, or WKT string

Parameters:
- value (str) - An EPSG, PROJ, or WKT string.
- morph_from_esri_dialect (bool, optional) - If True, items in the input using Esri's dialect of WKT will be replaced by OGC standard equivalents.

Return type: CRS

Raises: CRSError

**static from_user_input(value, morph_from_esri_dialect=False)**
Make a CRS from a variety of inputs.

Parameters:
- value (object) - User input of many different kinds.
- morph_from_esri_dialect (bool, optional) - If True, items in the input using Esri's dialect of WKT will be replaced by OGC standard equivalents.

Return type: CRS

Raises: CRSError

**static from_wkt(wkt, morph_from_esri_dialect=False)**
Make a CRS from a WKT string.

Parameters:
- wkt (str) - A WKT string.
- morph_from_esri_dialect (bool, optional) - If True, items in the input using Esri's dialect of WKT will be replaced by OGC standard equivalents.

Return type: CRS

Raises: CRSError

**is_epsg_code**
Test if the CRS is defined by an EPSG code.

Return type: bool

**is_geographic**
Test if the CRS is a geographic coordinate reference system.

Return type: bool

Raises: CRSError

**is_projected**
Test if the CRS is a projected coordinate reference system.

Return type: bool

Raises: CRSError

**is_valid**
Test that the CRS is a geographic or projected CRS.

Deprecated since version 1.4.0: This property is not useful and will be removed in 2.0.0.

Return type: bool

**linear_units**
Get a short name for the linear units of the CRS.

Returns: units - "m", "ft", etc. (str)

Raises: CRSError

**linear_units_factor**
Get linear units and the conversion factor to meters of the CRS.

Returns:
- units (str) - "m", "ft", etc.
- factor (float) - Ratio of one unit to one meter.

Raises: CRSError

**to_authority(self, confidence_threshold=70)**
Convert to the best match authority name and code.

For a CRS created using an EPSG code, that same value is returned. For other CRS, including custom CRS, an attempt is made to match it to definitions in authority files. Matches with a confidence below the threshold are discarded.

Parameters:
- confidence_threshold (int) - Percent match confidence threshold (0-100).

Returns:
- name (str) - Authority name.
- code (str) - Code from the authority file.
- or None

**to_dict(self, projjson=False)**
Convert CRS to a PROJ dict.

Note: If there is a corresponding EPSG code, it will be used when returning PROJ parameter dict.

Parameters:
- projjson (bool, default=False) - If True, will convert to PROJ JSON dict (Requires GDAL 3.1+ and PROJ 6.2+). If False, will convert to PROJ parameter dict.

Return type: dict

**to_epsg(self, confidence_threshold=70)**
Convert to the best match EPSG code.

For a CRS created using an EPSG code, that same value is returned. For other CRS, including custom CRS, an attempt is made to match it to definitions in the EPSG authority file. Matches with a confidence below the threshold are discarded.

Parameters:
- confidence_threshold (int) - Percent match confidence threshold (0-100).

Return type: int or None

Raises: CRSError

**to_proj4(self)**
Convert to a PROJ4 representation.

Return type: str

**to_string(self)**
Convert to a PROJ4 or WKT string.

The output will be reduced as much as possible by attempting a match to CRS defined in authority files.

Notes: Mapping keys are tested against the all_proj_keys list. Values of True are omitted, leaving the key bare: {'no_defs': True} -> "+no_defs" and items where the value is otherwise not a str, int, or float are omitted.

Return type: str

Raises: CRSError

**to_wkt(self, morph_to_esri_dialect=False, version=None)**
Convert to a OGC WKT representation.

Parameters:
- morph_to_esri_dialect (bool, optional) - Whether or not to morph to the Esri dialect of WKT. Only applies to GDAL versions < 3. This parameter will be removed in a future version of rasterio.
- version (WktVersion or str, optional) - The version of the WKT output. Only works with GDAL 3+. Default is WKT1_GDAL.

Return type: str

Raises: CRSError

**units_factor**
Get units and the conversion factor of the CRS.

Returns:
- units (str) - "m", "ft", etc.
- factor (float) - Ratio of one unit to one radian if the CRS is geographic otherwise, it is to one meter.

Raises: CRSError

**wkt**
An OGC WKT representation of the CRS.

Return type: str

## rasterio.crs.epsg_treats_as_latlong(input_crs)

Test if the CRS is in latlon order.

From GDAL docs:
> This method returns TRUE if EPSG feels this geographic coordinate system should be treated as having lat/long coordinate ordering.
> Currently this returns TRUE for all geographic coordinate systems with an EPSG code set, and axes set defining it as lat, long.
> FALSE will be returned for all coordinate systems that are not geographic, or that do not have an EPSG code set.
>
> Note: Important change of behavior since GDAL 3.0. In previous versions, geographic CRS imported with importFromEPSG() would cause this method to return FALSE on them, whereas now it returns TRUE, since importFromEPSG() is now equivalent to importFromEPSGA().

Parameters:
- input_crs (CRS) - Coordinate reference system, as a rasterio CRS object. Example: CRS({'init': 'EPSG:4326'})

Return type: bool

## rasterio.crs.epsg_treats_as_northingeasting(input_crs)

Test if the CRS should be treated as having northing/easting coordinate ordering.

From GDAL docs:
> This method returns TRUE if EPSG feels this projected coordinate system should be treated as having northing/easting coordinate ordering.
> Currently this returns TRUE for all projected coordinate systems with an EPSG code set, and axes set defining it as northing, easting.
> FALSE will be returned for all coordinate systems that are not projected, or that do not have an EPSG code set.
>
> Note: Important change of behavior since GDAL 3.0. In previous versions, projected CRS with northing, easting axis order imported with importFromEPSG() would cause this method to return FALSE on them, whereas now it returns TRUE, since importFromEPSG() is now equivalent to importFromEPSGA().

Parameters:
- input_crs (CRS) - Coordinate reference system, as a rasterio CRS object. Example: CRS({'init': 'EPSG:4326'})

Return type: bool
