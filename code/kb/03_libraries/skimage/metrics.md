# scikit-image Metrics: Image Comparison (skimage.metrics)

Source: https://scikit-image.org/docs/stable/api/skimage.metrics.html

Image comparison and quality metrics for evaluating similarity between images.

## Functions

### `mean_squared_error(image0, image1)`

Compute the mean-squared error between two images.

**Parameters:**
- `image0, image1` ndarray: Images. Any dimensionality, must have same shape.

**Returns:**
- `mse` float: The mean-squared error (MSE) metric.

---

### `normalized_root_mse(image_true, image_test, *, normalization='euclidean')`

Compute the normalized root mean-squared error (NRMSE) between two images.

**Parameters:**
- `image_true` ndarray: Ground-truth image, same shape as im_test.
- `image_test` ndarray: Test image.
- `normalization` {'euclidean', 'min-max', 'mean'}, optional: Controls the normalization method to use in the denominator of the NRMSE. There is no standard method of normalization across the literature. The methods available here are as follows:
  - 'euclidean' : normalize by the averaged Euclidean norm of im_true: `NRMSE = RMSE * sqrt(N) / || im_true ||` where || . || denotes the Frobenius norm and N = im_true.size. This result is equivalent to: `NRMSE = || im_true - im_test || / || im_true ||`.
  - 'min-max'   : normalize by the intensity range of im_true.
  - 'mean'      : normalize by the mean of im_true

**Returns:**
- `nrmse` float: The NRMSE metric.

---

### `peak_signal_noise_ratio(image_true, image_test, *, data_range=None)`

Compute the peak signal to noise ratio (PSNR) for an image.

**Parameters:**
- `image_true` ndarray: Ground-truth image, same shape as im_test.
- `image_test` ndarray: Test image.
- `data_range` int, optional: The data range of the input image (distance between minimum and maximum possible values). By default, this is estimated from the image data-type.

**Returns:**
- `psnr` float: The PSNR metric.

---

### `structural_similarity(im1, im2, *, win_size=None, gradient=False, data_range=None, channel_axis=None, gaussian_weights=False, full=False, **kwargs)`

Compute the mean structural similarity index between two images.
Please pay attention to the `data_range` parameter with floating-point images.

**Parameters:**
- `im1, im2` ndarray: Images. Any dimensionality with same shape.
- `win_size` int or None, optional: The side-length of the sliding window used in comparison. Must be an odd value. If `gaussian_weights` is True, this is ignored and the window size will depend on `sigma`.
- `gradient` bool, optional: If True, also return the gradient with respect to im2.
- `data_range` float, optional: The data range of the input image (difference between maximum and minimum possible values). By default, this is estimated from the image data type. This estimate may be wrong for floating-point image data. Therefore it is recommended to always pass this scalar value explicitly.
- `channel_axis` int or None, optional: If None, the image is assumed to be a grayscale (single channel) image. Otherwise, this parameter indicates which axis of the array corresponds to channels.
- `gaussian_weights` bool, optional: If True, each patch has its mean and variance spatially weighted by a normalized Gaussian kernel of width sigma=1.5.
- `full` bool, optional: If True, also return the full structural similarity image.

**Other Parameters:**
- `use_sample_covariance` bool: If True, normalize covariances by N-1 rather than, N where N is the number of pixels within the sliding window.
- `K1` float: Algorithm parameter, K1 (small constant).
- `K2` float: Algorithm parameter, K2 (small constant).
- `sigma` float: Standard deviation for the Gaussian when `gaussian_weights` is True.

**Returns:**
- `mssim` float: The mean structural similarity index over the image.
- `grad` ndarray: The gradient of the structural similarity between im1 and im2. This is only returned if `gradient` is set to True.
- `S` ndarray: The full SSIM image. This is only returned if `full` is set to True.

**Notes:**
If `data_range` is not specified, the range is automatically guessed based on the image data type. However for floating-point image data, this estimate yields a result double the value of the desired range, as the `dtype_range` in `skimage.util.dtype.py` has defined intervals from -1 to +1. This yields an estimate of 2, instead of 1, which is most often required when working with image data (as negative light intensities are nonsensical).

To match the implementation of Wang et al., set `gaussian_weights` to True, `sigma` to 1.5, `use_sample_covariance` to False, and specify the `data_range` argument.

---

### `hausdorff_distance(image0, image1, method='standard')`

Calculate the Hausdorff distance between nonzero elements of given images.

**Parameters:**
- `image0, image1` ndarray: Arrays where `True` represents a point that is included in a set of points. Both arrays must have the same shape.
- `method` {'standard', 'modified'}, optional, default = 'standard': The method to use for calculating the Hausdorff distance. `standard` is the standard Hausdorff distance, while `modified` is the modified Hausdorff distance.

**Returns:**
- `distance` float: The Hausdorff distance between coordinates of nonzero pixels in `image0` and `image1`, using the Euclidean distance.

**Notes:**
The Hausdorff distance is the maximum distance between any point on `image0` and its nearest point on `image1`, and vice-versa. The Modified Hausdorff Distance (MHD) has been shown to perform better than the directed Hausdorff Distance (HD). The function calculates forward and backward mean distances and returns the largest of the two.

**Examples:**
```python
>>> points_a = (3, 0)
>>> points_b = (6, 0)
>>> shape = (7, 1)
>>> image_a = np.zeros(shape, dtype=bool)
>>> image_b = np.zeros(shape, dtype=bool)
>>> image_a[points_a] = True
>>> image_b[points_b] = True
>>> hausdorff_distance(image_a, image_b)
3.0
```

---

### `hausdorff_pair(image0, image1)`

Returns pair of points that are Hausdorff distance apart between nonzero elements of given images.

The Hausdorff distance is the maximum distance between any point on `image0` and its nearest point on `image1`, and vice-versa.

**Parameters:**
- `image0, image1` ndarray: Arrays where `True` represents a point that is included in a set of points. Both arrays must have the same shape.

**Returns:**
- `point_a, point_b` array: A pair of points that have Hausdorff distance between them.

**Examples:**
```python
>>> points_a = (3, 0)
>>> points_b = (6, 0)
>>> shape = (7, 1)
>>> image_a = np.zeros(shape, dtype=bool)
>>> image_b = np.zeros(shape, dtype=bool)
>>> image_a[points_a] = True
>>> image_b[points_b] = True
>>> hausdorff_pair(image_a, image_b)
(array([3, 0]), array([6, 0]))
```
