# scikit-image Region Measurements (skimage.measure)

Source: https://scikit-image.org/docs/stable/api/skimage.measure.html

Measurement of image properties, e.g., region properties, contours.

## Functions

### `approximate_polygon(coords, tolerance)`
Approximate a polygonal chain using the Douglas-Peucker algorithm within a specified tolerance.

**Parameters:**
- `coords` (K, 2) array: Coordinate array
- `tolerance` float: Maximum distance from original polygon points

**Returns:** (L, 2) array where L <= K

---

### `block_reduce(image, block_size=2, func=<function sum>, cval=0, func_kwargs=None)`
Downsample an image by applying a function to local blocks.

**Parameters:**
- `image` (M[, …]) ndarray: N-dimensional input image
- `block_size` array_like or int: Down-sampling factor (default: 2)
- `func` callable: Function implementing an `axis` parameter
- `cval` float: Padding value if image doesn't divide evenly
- `func_kwargs` dict: Keyword arguments for `func`

**Returns:** ndarray with same dimensions as input

---

### `blur_effect(image, h_size=11, channel_axis=None, reduce_func=<function max>)`
Compute blur strength metric (0=no blur, 1=maximal blur).

**Parameters:**
- `image` ndarray: RGB or grayscale nD image
- `h_size` int: Re-blurring filter size (default: 11)
- `channel_axis` int or None: Color channel axis
- `reduce_func` callable: Aggregation function

**Returns:** float between 0-1 (or list if reduce_func=None)

---

### `centroid(image, *, spacing=None)`
Return the weighted centroid of an image.

**Parameters:**
- `image` array: Input image
- `spacing` tuple of float: Pixel spacing along each axis

**Returns:** tuple of float - Centroid coordinates

---

### `euler_number(image, connectivity=None)`
Calculate the Euler characteristic in a binary image. For 2D: objects minus holes. For 3D: objects plus holes minus tunnels.

**Parameters:**
- `image` (M, N[, P]) ndarray: Binary input image
- `connectivity` int: Maximum orthogonal hops (1 to ndim)

**Returns:** int - Euler characteristic

---

### `find_contours(image, level=None, fully_connected='low', positive_orientation='low', *, mask=None)`
Find iso-valued contours using the marching squares algorithm.

**Parameters:**
- `image` (M, N) ndarray: Input image
- `level` float: Contour value (default: (max+min)/2)
- `fully_connected` {'low', 'high'}: Connectivity specification
- `positive_orientation` {'low', 'high'}: Orientation control
- `mask` (M, N) ndarray of bool: Region of interest

**Returns:** list of (K, 2) ndarrays - Contour coordinates

---

### `grid_points_in_poly(shape, verts, binarize=True)`
Test whether grid points are inside a polygon.

**Parameters:**
- `shape` tuple (M, N): Grid shape
- `verts` (V, 2) array: Polygon vertices
- `binarize` bool: Output type (True=boolean, False=labeled)

**Returns:** (M, N) ndarray - Boolean mask or labeled array

---

### `inertia_tensor(image, mu=None, *, spacing=None)`
Compute the inertia tensor of an input image.

**Parameters:**
- `image` array: Input image
- `mu` array: Pre-computed central moments (optional)
- `spacing` tuple of float: Pixel spacing

**Returns:** array shape (ndim, ndim) - Inertia tensor

---

### `inertia_tensor_eigvals(image, mu=None, T=None, *, spacing=None)`
Compute eigenvalues of the inertia tensor.

**Parameters:**
- `image` array: Input image
- `mu` array: Pre-computed central moments
- `T` array: Pre-computed inertia tensor
- `spacing` tuple of float: Pixel spacing

**Returns:** list of float - Eigenvalues in descending order

---

### `intersection_coeff(image0_mask, image1_mask, mask=None)`
Calculate the fraction of one mask overlapping with another.

**Parameters:**
- `image0_mask` (M, N) ndarray of bool: Channel A mask
- `image1_mask` (M, N) ndarray of bool: Channel B mask
- `mask` (M, N) ndarray of bool: Region of interest

**Returns:** float - Intersection coefficient

---

### `label(label_image, background=None, return_num=False, connectivity=None)`
Label connected regions of an integer array.

**Parameters:**
- `label_image` ndarray of int: Image to label
- `background` int: Background pixel value
- `return_num` bool: Whether to return label count
- `connectivity` int: Maximum orthogonal hops (1 to ndim)

**Returns:** ndarray of int (and optionally int count)

---

### `manders_coloc_coeff(image0, image1_mask, mask=None)`
Compute Manders' colocalization coefficient between channels.

**Parameters:**
- `image0` (M, N) ndarray: First channel
- `image1_mask` (M, N) ndarray of bool: Second channel mask
- `mask` (M, N) ndarray of bool: Region of interest

**Returns:** float - Manders' colocalization coefficient

---

### `manders_overlap_coeff(image0, image1, mask=None)`
Compute Manders' overlap coefficient between two channels.

**Parameters:**
- `image0` (M, N) ndarray: Channel A
- `image1` (M, N) ndarray: Channel B
- `mask` (M, N) ndarray of bool: Region of interest

**Returns:** float - Overlap coefficient

---

### `marching_cubes(volume, level=None, *, spacing=(1.0, 1.0, 1.0), gradient_direction='descent', step_size=1, allow_degenerate=True, method='lewiner', mask=None)`
Apply marching cubes algorithm to find 3D isosurfaces.

**Parameters:**
- `volume` (M, N, P) ndarray: Input volumetric data
- `level` float: Isosurface value
- `spacing` length-3 tuple: Voxel spacing
- `gradient_direction` {'descent', 'ascent'}: Gradient direction
- `step_size` int: Voxel steps (default: 1)
- `allow_degenerate` bool: Allow zero-area triangles
- `method` {'lewiner', 'lorensen'}: Algorithm choice
- `mask` (M, N, P) array: Boolean computation mask

**Returns:** verts (V, 3), faces (F, 3), normals (V, 3), values (V,) arrays

---

### `mesh_surface_area(verts, faces)`
Compute surface area from vertices and triangular faces.

**Parameters:**
- `verts` (V, 3) array: Mesh vertices
- `faces` (F, 3) array of ints: Triangle face indices

**Returns:** float - Surface area

---

### `moments(image, order=3, *, spacing=None)`
Calculate raw image moments up to specified order.

**Parameters:**
- `image` (N[, …]) array: Rasterized shape
- `order` int: Maximum moment order (default: 3)
- `spacing` tuple of float: Pixel spacing

**Returns:** (order+1, order+1) array - Raw moments

---

### `moments_central(image, center=None, order=3, *, spacing=None, **kwargs)`
Calculate central image moments up to specified order.

**Parameters:**
- `image` (N[, …]) array: Rasterized shape
- `center` tuple: Image centroid (auto-computed if None)
- `order` int: Maximum moment order (default: 3)
- `spacing` tuple of float: Pixel spacing

**Returns:** (order+1, order+1) array - Central moments

---

### `moments_coords(coords, order=3)`
Calculate raw moments from coordinate array.

**Parameters:**
- `coords` (N, D) array: N points in D-dimensional space
- `order` int: Maximum moment order (default: 3)

**Returns:** (order+1, order+1, …) array - Raw moments

---

### `moments_coords_central(coords, center=None, order=3)`
Calculate central moments from coordinate array.

**Parameters:**
- `coords` (N, D) array: N points in D dimensions
- `center` tuple: Centroid (auto-computed if None)
- `order` int: Maximum moment order (default: 3)

**Returns:** (order+1, order+1, …) array - Central moments

---

### `moments_hu(nu)`
Calculate Hu's invariant moments (2D-only, translation/scale/rotation invariant).

**Parameters:**
- `nu` (M, M) array: Normalized central moments where M >= 4

**Returns:** (7,) array - Hu's moment set

---

### `moments_normalized(mu, order=3, spacing=None)`
Calculate normalized central moments up to specified order.

**Parameters:**
- `mu` (M[, …], M) array: Central moments
- `order` int: Maximum moment order (default: 3)
- `spacing` tuple of float: Pixel spacing

**Returns:** (order+1[, ...], order+1) array - Normalized moments

---

### `pearson_corr_coeff(image0, image1, mask=None)`
Calculate Pearson's correlation coefficient between channel intensities.

**Parameters:**
- `image0` (M, N) ndarray: Channel A
- `image1` (M, N) ndarray: Channel B
- `mask` (M, N) ndarray of bool: Region of interest

**Returns:** tuple - (pcc: float, p-value: float)

---

### `perimeter(image, neighborhood=4)`
Calculate total perimeter of objects in binary image.

**Parameters:**
- `image` (M, N) ndarray: Binary input
- `neighborhood` {4, 8}: Connectivity (default: 4)

**Returns:** float - Total perimeter

---

### `perimeter_crofton(image, directions=4)`
Calculate Crofton perimeter using integral geometry.

**Parameters:**
- `image` (M, N) ndarray: Binary input
- `directions` {2, 4}: Approximation directions (default: 4)

**Returns:** float - Crofton perimeter

---

### `points_in_poly(points, verts)`
Test whether points lie inside a polygon.

**Parameters:**
- `points` (K, 2) array: (x, y) coordinates
- `verts` (L, 2) array: Polygon vertices

**Returns:** (K,) array of bool - Inside polygon mask

---

### `profile_line(image, src, dst, linewidth=1, order=None, mode='reflect', cval=0.0, *, reduce_func=<function mean>)`
Return intensity profile along a scan line.

**Parameters:**
- `image` ndarray: Grayscale or multichannel
- `src` array_like (2,): Scan line start
- `dst` array_like (2,): Scan line end
- `linewidth` int: Perpendicular width (default: 1)
- `order` int in {0-5}: Spline interpolation order
- `mode` {'constant', 'nearest', 'reflect', 'mirror', 'wrap'}: Boundary handling
- `cval` float: Constant value for 'constant' mode
- `reduce_func` callable: Aggregation perpendicular to line

**Returns:** array - Intensity profile

---

### `ransac(data, model_class, min_samples, residual_threshold, is_data_valid=None, is_model_valid=None, max_trials=100, stop_sample_num=inf, stop_residuals_sum=0, stop_probability=1, rng=None, initial_inliers=None)`
Fit model using RANSAC (random sample consensus) algorithm.

**Parameters:**
- `data` list/tuple/array: Dataset to fit
- `model_class` type: Model with `estimate` and `residuals` methods
- `min_samples` int: Minimum samples for estimation
- `residual_threshold` float: Inlier classification threshold
- `is_data_valid` callable: Validates random data subset
- `is_model_valid` callable: Validates estimated model
- `max_trials` int: Maximum iterations (default: 100)
- `stop_sample_num` int: Stop if inliers >= this value
- `stop_residuals_sum` float: Stop if sum of residuals <= this
- `stop_probability` float in [0,1]: Confidence threshold
- `rng` Generator or int: Random number generator
- `initial_inliers` array-like bool: Initial sample mask

**Returns:** tuple - (model, inliers array of bool)

---

### `regionprops(label_image, intensity_image=None, cache=True, *, extra_properties=None, spacing=None, offset=None)`
Measure properties of labeled image regions.

**Parameters:**
- `label_image` (M, N[, P]) ndarray: Label image (0=ignore)
- `intensity_image` (M, N[, P][, C]) ndarray: Intensity data
- `cache` bool: Cache computed properties (default: True)
- `extra_properties` iterable of callables: Custom properties
- `spacing` tuple of float: Pixel spacing per axis
- `offset` array-like int: Origin coordinates

**Returns:** list of RegionProperties objects

**Available Properties:** area, area_bbox, area_convex, area_filled, axis_major_length, axis_minor_length, bbox, centroid, centroid_local, centroid_weighted, centroid_weighted_local, coords, coords_scaled, eccentricity, equivalent_diameter_area, euler_number, extent, feret_diameter_max, image, image_convex, image_filled, image_intensity, inertia_tensor, inertia_tensor_eigvals, intensity_max, intensity_mean, intensity_median, intensity_min, intensity_std, label, moments, moments_central, moments_hu, moments_normalized, moments_weighted, moments_weighted_central, moments_weighted_hu, moments_weighted_normalized, num_pixels, orientation, perimeter, perimeter_crofton, slice, solidity

---

### `regionprops_table(label_image, intensity_image=None, properties=('label', 'bbox'), *, cache=True, separator='-', extra_properties=None, spacing=None)`
Compute region properties as a pandas-compatible table.

**Parameters:**
- `label_image` (M, N[, P]) ndarray: Label image
- `intensity_image` (M, N[, P][, C]) ndarray: Intensity data
- `properties` tuple/list of str: Properties to include
- `cache` bool: Cache computed properties (default: True)
- `separator` str: For non-scalar properties not listed in OBJECT_COLUMNS, each element will appear in its own column, with the index of that element separated from the property name by this separator (default: '-')
- `extra_properties` iterable of callables: Custom properties
- `spacing` tuple of float: Pixel spacing

**Returns:** dict - Property names mapped to value arrays

---

### `shannon_entropy(image, base=2)`
Calculate Shannon entropy of an image.

**Parameters:**
- `image` (M, N) ndarray: Grayscale input
- `base` float: Logarithmic base (default: 2)

**Returns:** float - Entropy value

---

### `subdivide_polygon(coords, degree=2, preserve_ends=False)`
Subdivide polygonal curves using B-splines.

**Parameters:**
- `coords` (K, 2) array: Coordinate array
- `degree` {1-7}: B-spline degree (default: 2)
- `preserve_ends` bool: Preserve endpoints (default: False)

**Returns:** (L, 2) array - Subdivided coordinates

---

## Classes

### `CircleModel`
Total least squares estimator for 2D circles.

**Key Methods:**
- `estimate(data)` - Estimate model parameters from data
- `residuals(data)` - Calculate residuals to fitted circle
- `predict_xy(t, params=None)` - Predict x and y coordinates using the estimated model

---

### `EllipseModel`
Total least squares estimator for 2D ellipses.

**Key Methods:**
- `estimate(data)` - Estimate model parameters from data
- `residuals(data)` - Return residuals of data to model
- `predict_xy(t, params=None)` - Predict x and y coordinates using estimated model

---

### `LineModelND`
Total least squares estimator for N-dimensional lines.

**Key Methods:**
- `estimate(data)` - Estimate model parameters from data
- `residuals(data, params=None)` - Return residuals of data to model
- `predict(x, axis=0, params=None)` - Predict intersecting coordinates using estimated model

---

### `RansacModelProtocol`
Protocol specifying interface for RANSAC model classes. Requires `estimate` and `residuals` methods.
