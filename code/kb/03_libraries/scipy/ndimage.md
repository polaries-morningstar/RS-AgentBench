# SciPy N-dimensional Image Processing (scipy.ndimage)

Source: https://docs.scipy.org/doc/scipy/reference/ndimage.html

# Multidimensional image processing (scipy.ndimage)

This package contains various functions for multidimensional image processing.

## Filters

`convolve(input, weights[, output, mode, ...])`
Multidimensional convolution.

`convolve1d(input, weights[, axis, output, ...])`
Calculate a 1-D convolution along the given axis.

`correlate(input, weights[, output, mode, ...])`
Multidimensional correlation.

`correlate1d(input, weights[, axis, output, ...])`
Calculate a 1-D correlation along the given axis.

`gaussian_filter(input, sigma[, order, ...])`
Multidimensional Gaussian filter.

`gaussian_filter1d(input, sigma[, axis, ...])`
1-D Gaussian filter.

`gaussian_gradient_magnitude(input, sigma[, ...])`
Multidimensional gradient magnitude using Gaussian derivatives.

`gaussian_laplace(input, sigma[, output, ...])`
Multidimensional Laplace filter using Gaussian second derivatives.

`generic_filter(input, function[, size, ...])`
Calculate a multidimensional filter using the given function.

`generic_filter1d(input, function, filter_size)`
Calculate a 1-D filter along the given axis.

`generic_gradient_magnitude(input, derivative)`
Gradient magnitude using a provided gradient function.

`generic_laplace(input, derivative2[, ...])`
N-D Laplace filter using a provided second derivative function.

`laplace(input[, output, mode, cval, axes])`
N-D Laplace filter based on approximate second derivatives.

`maximum_filter(input[, size, footprint, ...])`
Calculate a multidimensional maximum filter.

`maximum_filter1d(input, size[, axis, ...])`
Calculate a 1-D maximum filter along the given axis.

`median_filter(input[, size, footprint, ...])`
Calculate a multidimensional median filter.

`minimum_filter(input[, size, footprint, ...])`
Calculate a multidimensional minimum filter.

`minimum_filter1d(input, size[, axis, ...])`
Calculate a 1-D minimum filter along the given axis.

`percentile_filter(input, percentile[, size, ...])`
Calculate a multidimensional percentile filter.

`prewitt(input[, axis, output, mode, cval])`
Calculate a Prewitt filter.

`rank_filter(input, rank[, size, footprint, ...])`
Calculate a multidimensional rank filter.

`sobel(input[, axis, output, mode, cval])`
Calculate a Sobel filter.

`uniform_filter(input[, size, output, mode, ...])`
Multidimensional uniform filter.

`uniform_filter1d(input, size[, axis, ...])`
Calculate a 1-D uniform filter along the given axis.

`vectorized_filter(input, function, *[, ...])`
Filter an array with a vectorized Python callable as the kernel

## Fourier filters

`fourier_ellipsoid(input, size[, n, axis, output])`
Multidimensional ellipsoid Fourier filter.

`fourier_gaussian(input, sigma[, n, axis, output])`
Multidimensional Gaussian fourier filter.

`fourier_shift(input, shift[, n, axis, output])`
Multidimensional Fourier shift filter.

`fourier_uniform(input, size[, n, axis, output])`
Multidimensional uniform fourier filter.

## Interpolation

`affine_transform(input, matrix[, offset, ...])`
Apply an affine transformation.

`geometric_transform(input, mapping[, ...])`
Apply an arbitrary geometric transform.

`map_coordinates(input, coordinates[, ...])`
Map the input array to new coordinates by interpolation.

`rotate(input, angle[, axes, reshape, ...])`
Rotate an array.

`shift(input, shift[, output, order, mode, ...])`
Shift an array.

`spline_filter(input[, order, output, mode])`
Multidimensional spline filter.

`spline_filter1d(input[, order, axis, ...])`
Calculate a 1-D spline filter along the given axis.

`zoom(input, zoom[, output, order, mode, ...])`
Zoom an array.

## Measurements

`center_of_mass(input[, labels, index])`
Calculate the center of mass of the values of an array at labels.

`extrema(input[, labels, index])`
Calculate the minimums and maximums of the values of an array at labels, along with their positions.

`find_objects(input[, max_label])`
Find objects in a labeled array.

`histogram(input, min, max, bins[, labels, index])`
Calculate the histogram of the values of an array, optionally at labels.

`label(input[, structure, output])`
Label features in an array.

`labeled_comprehension(input, labels, index, ...)`
Roughly equivalent to [func(input[labels == i]) for i in index].

`maximum(input[, labels, index])`
Calculate the maximum of the values of an array over labeled regions.

`maximum_position(input[, labels, index])`
Find the positions of the maximums of the values of an array at labels.

`mean(input[, labels, index])`
Calculate the mean of the values of an array at labels.

`median(input[, labels, index])`
Calculate the median of the values of an array over labeled regions.

`minimum(input[, labels, index])`
Calculate the minimum of the values of an array over labeled regions.

`minimum_position(input[, labels, index])`
Find the positions of the minimums of the values of an array at labels.

`standard_deviation(input[, labels, index])`
Calculate the standard deviation of the values of an N-D image array, optionally at specified sub-regions.

`sum_labels(input[, labels, index])`
Calculate the sum of the values of the array.

`value_indices(arr, *[, ignore_value])`
Find indices of each distinct value in given array.

`variance(input[, labels, index])`
Calculate the variance of the values of an N-D image array, optionally at specified sub-regions.

`watershed_ift(input, markers[, structure, ...])`
Apply watershed from markers using image foresting transform algorithm.

## Morphology

`binary_closing(input[, structure, ...])`
Multidimensional binary closing with the given structuring element.

`binary_dilation(input[, structure, ...])`
Multidimensional binary dilation with the given structuring element.

`binary_erosion(input[, structure, ...])`
Multidimensional binary erosion with a given structuring element.

`binary_fill_holes(input[, structure, ...])`
Fill the holes in binary objects.

`binary_hit_or_miss(input[, structure1, ...])`
Multidimensional binary hit-or-miss transform.

`binary_opening(input[, structure, ...])`
Multidimensional binary opening with the given structuring element.

`binary_propagation(input[, structure, mask, ...])`
Multidimensional binary propagation with the given structuring element.

`black_tophat(input[, size, footprint, ...])`
Multidimensional black tophat filter.

`distance_transform_bf(input[, metric, ...])`
Distance transform function by a brute force algorithm.

`distance_transform_cdt(input[, metric, ...])`
Distance transform for chamfer type of transforms.

`distance_transform_edt(input[, sampling, ...])`
Exact Euclidean distance transform.

`generate_binary_structure(rank, connectivity)`
Generate a binary structure for binary morphological operations.

`grey_closing(input[, size, footprint, ...])`
Multidimensional grayscale closing.

`grey_dilation(input[, size, footprint, ...])`
Calculate a greyscale dilation, using either a structuring element, or a footprint corresponding to a flat structuring element.

`grey_erosion(input[, size, footprint, ...])`
Calculate a greyscale erosion, using either a structuring element, or a footprint corresponding to a flat structuring element.

`grey_opening(input[, size, footprint, ...])`
Multidimensional grayscale opening.

`iterate_structure(structure, iterations[, ...])`
Iterate a structure by dilating it with itself.

`morphological_gradient(input[, size, ...])`
Multidimensional morphological gradient.

`morphological_laplace(input[, size, ...])`
Multidimensional morphological laplace.

`white_tophat(input[, size, footprint, ...])`
Multidimensional white tophat filter.
