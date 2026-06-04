# scikit-image Exposure & Histogram Operations (skimage.exposure)

Source: https://scikit-image.org/docs/stable/api/skimage.exposure.html
Source: https://scikit-image.org/docs/stable/auto_examples/color_exposure/plot_histogram_matching.html

skimage.exposure#


Image intensity adjustment, e.g., histogram equalization, etc.


adjust_gamma


Perform gamma correction on the input image.


adjust_log


Performs Logarithmic correction on the input image.


adjust_sigmoid


Performs Sigmoid Correction on the input image.


cumulative_distribution


Return cumulative distribution function (cdf) for the given image.


equalize_adapthist


Contrast Limited Adaptive Histogram Equalization (CLAHE).


equalize_hist


Return image after histogram equalization.


histogram


Return histogram of image.


is_low_contrast


Determine if an image is low contrast.


match_histograms


Adjust an image so that its cumulative histogram matches that of another.


rescale_intensity


Return image after stretching or shrinking its intensity levels.


skimage.exposure.adjust_gamma(image, gamma=1, gain=1)[source]#


Perform gamma correction on the input image.


Gamma correction is a power-law transform [1]. This function
transforms the input 
image pixel-wise according to the power law

image**gamma after scaling each pixel to the range 0 to 1. Then
it is rescaled to its original range and muliplied by 
gain.


Parameters:


imagendarray

Input image.


gammafloat, optional

Non negative real number. Default value is 1.


gainfloat, optional

The constant multiplier. Default value is 1.


Returns:


outndarray

Gamma corrected output image.


See also


adjust_log


Notes


For gamma greater than 1, the histogram will shift towards left and
the output image will be darker than the input image.


For gamma less than 1, the histogram will shift towards right and
the output image will be brighter than the input image.


References


[1]

https://en.wikipedia.org/wiki/Gamma_correction


Examples


>>> import skimage as ski
>>> image = ski.util.img_as_float(ski.data.moon())
>>> gamma_corrected = ski.exposure.adjust_gamma(image, 2)
>>> # Output is darker for gamma > 1
>>> image.mean() > gamma_corrected.mean()
True


Explore 3D images (of cells)

  Explore 3D images (of cells)


Gamma and log contrast adjustment

  Gamma and log contrast adjustment


skimage.exposure.adjust_log(image, gain=1, inv=False)[source]#


Performs Logarithmic correction on the input image.


This function transforms the input image pixelwise according to the
equation 
O = gain*log(1 + I) after scaling each pixel to the range
0 to 1. For inverse logarithmic correction, the equation is

O = gain*(2**I - 1).


Parameters:


imagendarray

Input image.


gainfloat, optional

The constant multiplier. Default value is 1.


invfloat, optional

If True, it performs inverse logarithmic correction,
else correction will be logarithmic. Defaults to False.


Returns:


outndarray

Logarithm corrected output image.


See also


adjust_gamma


References


[1]

http://www.ece.ucsb.edu/Faculty/Manjunath/courses/ece178W03/EnhancePart1.pdf


Gamma and log contrast adjustment

  Gamma and log contrast adjustment


skimage.exposure.adjust_sigmoid(image, cutoff=0.5, gain=10, inv=False)[source]#


Performs Sigmoid Correction on the input image.


Also known as Contrast Adjustment.
This function transforms the input image pixelwise according to the
equation 
O = 1/(1 + exp*(gain*(cutoff - I))) after scaling each pixel
to the range 0 to 1.


Parameters:


imagendarray

Input image.


cutofffloat, optional

Cutoff of the sigmoid function that shifts the characteristic curve
in horizontal direction. Default value is 0.5.


gainfloat, optional

The constant multiplier in exponential's power of sigmoid function.
Default value is 10.


invbool, optional

If True, returns the negative sigmoid correction. Defaults to False.


Returns:


outndarray

Sigmoid corrected output image.


See also


adjust_gamma


References


[1]

Gustav J. Braun, "Image Lightness Rescaling Using Sigmoidal Contrast
Enhancement Functions",
http://markfairchild.org/PDFs/PAP07.pdf


skimage.exposure.cumulative_distribution(image, nbins=256)[source]#


Return cumulative distribution function (cdf) for the given image.


Parameters:


imagearray

Image array.


nbinsint, optional

Number of bins for image histogram.


Returns:


img_cdfarray

Values of cumulative distribution function.


bin_centersarray

Centers of bins.


See also


histogram


References


[1]

https://en.wikipedia.org/wiki/Cumulative_distribution_function


Examples


>>> from skimage import data, exposure, img_as_float
>>> image = img_as_float(data.camera())
>>> hi = exposure.histogram(image)
>>> cdf = exposure.cumulative_distribution(image)
>>> all(cdf[0] == np.cumsum(hi[0])/float(image.size))
True


Explore 3D images (of cells)

  Explore 3D images (of cells)


Histogram Equalization

  Histogram Equalization


Histogram matching

  Histogram matching


Local Histogram Equalization

  Local Histogram Equalization


Gamma and log contrast adjustment

  Gamma and log contrast adjustment


skimage.exposure.equalize_adapthist(image, kernel_size=None, clip_limit=0.01, nbins=256)[source]#


Contrast Limited Adaptive Histogram Equalization (CLAHE).


An algorithm for local contrast enhancement, that uses histograms computed
over different tile regions of the image. Local details can therefore be
enhanced even in regions that are darker or lighter than most of the image.


Parameters:


image(M[, …][, C]) ndarray

Input image.


kernel_sizeint or array_like, optional

Defines the shape of contextual regions used in the algorithm. If
iterable is passed, it must have the same number of elements as

image.ndim (without color channel). If integer, it is broadcasted
to each 
image dimension. By default, 
kernel_size is 1/8 of

image height by 1/8 of its width.


clip_limitfloat, optional

Clipping limit, normalized between 0 and 1 (higher values give more
contrast).


nbinsint, optional

Number of gray bins for histogram ("data range").


Returns:


out(M[, …][, C]) ndarray

Equalized image with float64 dtype.


See also


equalize_hist, 
rescale_intensity


Notes


For color images, the following steps are performed:


The image is converted to HSV color space


The CLAHE algorithm is run on the V (Value) channel


The image is converted back to RGB space and returned


For RGBA images, the original alpha channel is removed.


Changed in version 0.17: The values returned by this function are slightly shifted upwards
because of an internal change in rounding behavior.


References


[1]

http://tog.acm.org/resources/GraphicsGems/


[2]

https://en.wikipedia.org/wiki/CLAHE#CLAHE


3D adaptive histogram equalization

  3D adaptive histogram equalization


Histogram Equalization

  Histogram Equalization


skimage.exposure.equalize_hist(image, nbins=256, mask=None)[source]#


Return image after histogram equalization.


Parameters:


imagearray

Image array.


nbinsint, optional

Number of bins for image histogram. Note: this argument is
ignored for integer images, for which each integer is its own
bin.


maskndarray of bools or 0s and 1s, optional

Array of same shape as 
image. Only points at which mask == True
are used for the equalization, which is applied to the whole image.


Returns:


outfloat array

Image array after histogram equalization.


Notes


This function is adapted from [1] with the author's permission.


References


[1]

http://www.janeriksolem.net/histogram-equalization-with-python-and.html


[2]

https://en.wikipedia.org/wiki/Histogram_equalization


Explore 3D images (of cells)

  Explore 3D images (of cells)


Visual image comparison

  Visual image comparison


Rank filters

  Rank filters


3D adaptive histogram equalization

  3D adaptive histogram equalization


Histogram Equalization

  Histogram Equalization


Local Histogram Equalization

  Local Histogram Equalization


skimage.exposure.histogram(image, nbins=256, source_range='image', normalize=False, *, channel_axis=None)[source]#


Return histogram of image.


Unlike 
numpy.histogram, this function returns the centers of bins and
does not rebin integer arrays. For integer arrays, each integer value has
its own bin, which improves speed and intensity-resolution.


If 
channel_axis is not set, the histogram is computed on the flattened
image. For color or multichannel images, set 
channel_axis to use a
common binning for all channels. Alternatively, one may apply the function
separately on each channel to obtain a histogram for each color channel
with separate binning.


Parameters:


imagearray

Input image.


nbinsint, optional

Number of bins used to calculate histogram. This value is ignored for
integer arrays.


source_range{'image', 'dtype'}, optional

'image' (default) determines the range from the input image.
'dtype' determines the range from the expected range of the images
of that data type.


normalizebool, optional

If True, normalize the histogram by the sum of its values.


channel_axisint or None, optional

If None, the image is assumed to be a grayscale (single channel) image.
Otherwise, this parameter indicates which axis of the array corresponds
to channels.


Returns:


histarray

The values of the histogram. When 
channel_axis is not None, hist
will be a 2D array where the first axis corresponds to channels.


bin_centersarray

The values at the center of the bins.


See also


cumulative_distribution


Examples


>>> from skimage import data, exposure, img_as_float
>>> image = img_as_float(data.camera())
>>> np.histogram(image, bins=2)
(array([ 93585, 168559]), array([0. , 0.5, 1. ]))
>>> exposure.histogram(image, nbins=2)
(array([ 93585, 168559]), array([0.25, 0.75]))


Comparing edge-based and region-based segmentation

  Comparing edge-based and region-based segmentation


Rank filters

  Rank filters


Histogram matching

  Histogram matching


skimage.exposure.is_low_contrast(image, fraction_threshold=0.05, lower_percentile=1, upper_percentile=99, method='linear')[source]#


Determine if an image is low contrast.


Parameters:


imagearray-like

The image under test.


fraction_thresholdfloat, optional

The low contrast fraction threshold. An image is considered low-
contrast when its range of brightness spans less than this
fraction of its data type's full range. [1]


lower_percentilefloat, optional

Disregard values below this percentile when computing image contrast.


upper_percentilefloat, optional

Disregard values above this percentile when computing image contrast.


methodstr, optional

The contrast determination method.  Right now the only available
option is "linear".


Returns:


outbool

True when the image is determined to be low contrast.


Notes


For boolean images, this function returns False only if all values are
the same (the method, threshold, and percentile arguments are ignored).


References


[1]

https://scikit-image.org/docs/dev/user_guide/data_types.html


Examples


>>> image = np.linspace(0, 0.04, 100)
>>> is_low_contrast(image)
True
>>> image[-1] = 1
>>> is_low_contrast(image)
True
>>> is_low_contrast(image, upper_percentile=100)
False


skimage.exposure.match_histograms(image, reference, *, channel_axis=None)[source]#


Adjust an image so that its cumulative histogram matches that of another.


The adjustment is applied separately for each channel.


Parameters:


imagendarray

Input image. Can be gray-scale or in color.


referencendarray

Image to match histogram of. Must have the same number of channels as
image.


channel_axisint or None, optional

If None, the image is assumed to be a grayscale (single channel) image.
Otherwise, this parameter indicates which axis of the array corresponds
to channels.


Returns:


matchedndarray

Transformed input image.


Raises:


ValueError

Thrown when the number of channels in the input image and the reference
differ.


References


[1]

http://paulbourke.net/miscellaneous/equalisation/


Histogram matching

  Histogram matching


skimage.exposure.rescale_intensity(image, in_range='image', out_range='dtype')[source]#


Return image after stretching or shrinking its intensity levels.


The desired intensity range of the input and output, 
in_range and

out_range respectively, are used to stretch or shrink the intensity range
of the input image. See examples below.


Parameters:


imagearray

Image array.


in_range, out_rangestr or 2-tuple, optional

Min and max intensity values of input and output image.
The possible values for this parameter are enumerated below.


'image'

Use image min/max as the intensity range.


'dtype'

Use min/max of the image's dtype as the intensity range.


dtype-name

Use intensity range based on desired 
dtype. Must be valid key
in 
DTYPE_RANGE.


2-tuple

Use 
range_values as explicit min/max intensities.


Returns:


outarray

Image array after rescaling its intensity. This image is the same dtype
as the input image.


See also


equalize_hist


Notes


Changed in version 0.17: The dtype of the output array has changed to match the input dtype, or
float if the output range is specified by a pair of values.


Examples


By default, the min/max intensities of the input image are stretched to
the limits allowed by the image's dtype, since 
in_range defaults to
'image' and 
out_range defaults to 'dtype':


>>> image = np.array([51, 102, 153], dtype=np.uint8)
>>> rescale_intensity(image)
array([  0, 127, 255], dtype=uint8)


It's easy to accidentally convert an image dtype from uint8 to float:


>>> 1.0 * image
array([ 51., 102., 153.])


Use 
rescale_intensity to rescale to the proper range for float dtypes:


>>> image_float = 1.0 * image
>>> rescale_intensity(image_float)
array([0. , 0.5, 1. ])


To maintain the low contrast of the original, use the 
in_range parameter:


>>> rescale_intensity(image_float, in_range=(0, 255))
array([0.2, 0.4, 0.6])


If the min/max value of 
in_range is more/less than the min/max image
intensity, then the intensity levels are clipped:


>>> rescale_intensity(image_float, in_range=(0, 102))
array([0.5, 1. , 1. ])


If you have an image with signed integers but want to rescale the image to
just the positive range, use the 
out_range parameter. In that case, the
output dtype will be float:


>>> image = np.array([-10, 0, 10], dtype=np.int8)
>>> rescale_intensity(image, out_range=(0, 127))
array([  0. ,  63.5, 127. ])


To get the desired range with a specific dtype, use 
.astype():


>>> rescale_intensity(image, out_range=(0, 127)).astype(np.int8)
array([  0,  63, 127], dtype=int8)


If the input image is constant, the output will be clipped directly to the
output range:
>>> image = np.array([130, 130, 130], dtype=np.int32)
>>> rescale_intensity(image, out_range=(0, 127)).astype(np.int32)
array([127, 127, 127], dtype=int32)


Explore 3D images (of cells)

  Explore 3D images (of cells)


Rank filters

  Rank filters


Adapting gray-scale filters to RGB images

  Adapting gray-scale filters to RGB images


Histogram Equalization

  Histogram Equalization


Separate colors in immunohistochemical staining

  Separate colors in immunohistochemical staining


Histogram of Oriented Gradients

  Histogram of Oriented Gradients


Filling holes and finding peaks

  Filling holes and finding peaks


Phase Unwrapping

  Phase Unwrapping


Extrema

  Extrema


Random walker segmentation

  Random walker segmentation


Robust matching using RANSAC

  Robust matching using RANSAC


                

              
              
              
              
              
            

            
            
              
                
                


  

     On this page
  

  
    


adjust_gamma()


adjust_log()


adjust_sigmoid()


cumulative_distribution()


equalize_adapthist()


equalize_hist()


histogram()


is_low_contrast()


match_histograms()


rescale_intensity()

  


  
  
    
This Page

    
      
Show Source
    
   


              
            
          

          
            
          
        
      
    

  

  
  
  


  

  
    
      
        

  

    
      © Copyright 2013-2025, the scikit-image team.
      

    
  


      
    

  
  
  
    
      
        

  

    Created using Sphinx 8.2.3.
    

  


      
        


  
  Built with the PyData Sphinx Theme 0.16.1.

---

Histogram matching -- skimage 0.26.0 documentation
  
  
  
  
  
  
    
  
  
  
  


    
    
    
    
    
    
    
    
    
  
  
  
  
  


    
    
    
    
    
    
    
    
    
    
    
    
    
    
  
  
  
  
  
  
  

  
  
  Skip to main content

  
  

  
  
    Back to top

  
  
    

  
  
  Ctrl+K

  

  
  


  
    

  
    
  
  
  
  
    
      

  
     
  


  
  
  
  
  
    
    
      
    
    
    
    
  
  
    
scikit-image

  


    
  

  
  
    
    
      
        

  
    


  
    User guide
  


  
    Examples
  


  
    API reference
  


  
    Release notes
  


  
    Development
  


  
    About
  


  


      
    

    
    
    
      
        
          


 
 Search
 Ctrl+K

        

      
      
        

  
    Choose version  
    
  
  
    
  


      
        
        

          
          
          
          
          
          
          
          
          
            GitHub
        
        

          
          
          
          
          
          
          
          
          
            PyPI
        


      
    

    
  

  
  
    


 
 Search
 Ctrl+K

    

  

  
    
      
    
  


    
  

  
    
      
      
      
      
      
        

  
  
    
    
      
        
          
          
            

  
    


  
    User guide
  


  
    Examples
  


  
    API reference
  


  
    Release notes
  


  
    Development
  


  
    About
  


  


          
        
      

    
    
    
      
        
          

  
    Choose version  
    
  
  
    
  


        
          
        

          
          
          
          
          
          
          
          
          
            GitHub
        
        

          
          
          
          
          
          
          
          
          
            PyPI
        


        
      

    
  

  
    
        

  
Section Navigation

  

Data

Datasets with 3 or more spatial dimensions

Scientific images

General-purpose images

Specific images


Operations on NumPy arrays

Using simple NumPy operations for manipulating images

Generate footprints (structuring elements)

Block views on images/arrays

Decompose flat footprints (structuring elements)


Manipulating exposure and color channels

RGB to grayscale

RGB to HSV

Histogram matching

Adapting gray-scale filters to RGB images

Filtering regional maxima

Separate colors in immunohistochemical staining

Gamma and log contrast adjustment

Histogram Equalization

Tinting gray-scale images

Local Histogram Equalization

3D adaptive histogram equalization


Edges and lines

Contour finding

Convex Hull

Canny edge detector

Marching Cubes

Active Contour Model

Ridge operators

Shapes

Random Shapes

Approximate and subdivide polygons

Straight line Hough transform

Circular and Elliptical Hough Transforms

Skeletonize

Edge operators


Geometrical transformations and registration

Swirl

Interpolation: Edge Modes

Rescale, resize, and downscale

Build image pyramids

Piecewise Affine Transformation

Structural similarity index

Using geometric transformations

Types of homographies

Use thin-plate splines for image warping

Fundamental matrix estimation

Robust line model estimation using RANSAC

Radon transform

Robust matching using RANSAC


Image registration

Image Registration

Masked Normalized Cross-Correlation

Registration using optical flow

Assemble images with simple image stitching

Using Polar and Log-Polar Transformations for Registration


Filtering and restoration

Removing small objects in grayscale images with a top hat filter

Hysteresis thresholding

Image Deconvolution

Using window functions with images

Mean filters

Unsharp masking

Estimate strength of blur

Entropy

Image Deconvolution

Calibrating Denoisers Using J-Invariance

Fill in defects with inpainting

Band-pass filtering by Difference of Gaussians

Denoising a picture

Shift-invariant wavelet denoising

Phase Unwrapping

Non-local means denoising for preserving textures

Attribute operators

Wavelet denoising

Butterworth Filters

Full tutorial on calibrating Denoisers Using J-Invariance


Detection of features and objects

Dense DAISY feature description

Histogram of Oriented Gradients

Haar-like feature descriptor

Template Matching

Corner detection

Multi-Block Local Binary Pattern for texture classification

CENSURE feature detector

Filling holes and finding peaks

Removing objects

Blob Detection

ORB feature detector and binary descriptor

Gabors / Primary Visual Cortex "Simple Cells" from an Image

Fisher vector feature encoding

BRIEF binary descriptor

SIFT feature detector and descriptor extractor

GLCM Texture Features

Shape Index

Sliding window histogram

Gabor filter banks for texture classification

Local Binary Pattern for texture classification


Segmentation of objects

Region Boundary based Region adjacency graphs (RAGs)

Region adjacency graph (RAG) Thresholding

Normalized Cut

Find Regular Segments Using Compact Watershed

Thresholding

Drawing Region Adjacency Graphs (RAGs)

Chan-Vese Segmentation

Finding local maxima

Multi-Otsu Thresholding

Random walker segmentation

Apply maskSLIC vs SLIC

Niblack and Sauvola Thresholding

Expand segmentation labels without overlap

Watershed segmentation

Markers for watershed transform

Label image regions

Comparison of segmentation and superpixel algorithms

Find the intersection of two segmentations

Region Adjacency Graphs (RAGs)

Region adjacency graph (RAG) Merging

Measure perimeters with different estimators

Extrema

Explore and visualize region properties with pandas

Hausdorff Distance

Hierarchical Merging of Region Boundary RAGs

Morphological Snakes

Trainable segmentation using local features and random forests

Measure region properties

Evaluating segmentation metrics

Flood Fill

Use rolling-ball algorithm for estimating background intensity

Euler number


Longer examples and demonstrations

Render text onto an image

Face detection using a cascade classifier

Interact with 3D images (of kidney tissue)

Use pixel graphs to find an object's geodesic center

Visual image comparison

Morphological Filtering

Comparing edge-based and region-based segmentation

Estimate anisotropy in a 3D microscopy image

Colocalization metrics

Segment human cells (in mitosis)

Thresholding

Restore spotted cornea image with inpainting

Track solidification of a metallic alloy

Face classification using Haar-like feature descriptor

Measure fluorescence intensity at the nuclear envelope

Explore 3D images (of cells)

Rank filters


Examples for developers

Li thresholding

Max-tree


    

  
  
  
      


  


      

      
      
        
        
          
            
              
              

  
    
      
        


  
    
    

      
        
      
    
    
    
Examples
    
    
    
Manipulating exposure and color channels
    
    
Histogram matching
  


      
    

  
  


              
              
              
                


                
                  
  

Note


Go to the end
to download the full example code or to run this example in your browser via Binder.


Histogram matching#


This example demonstrates the feature of histogram matching. It manipulates the
pixels of an input image so that its histogram matches the histogram of the
reference image. If the images have multiple channels, the matching is done
independently for each channel, as long as the number of channels is equal in
the input image and the reference.


Histogram matching can be used as a lightweight normalisation for image
processing, such as feature matching, especially in circumstances where the
images have been taken from different sources or in different conditions (i.e.
lighting).


import matplotlib.pyplot as plt

from skimage import data
from skimage import exposure
from skimage.exposure import match_histograms

reference = data.coffee()
image = data.chelsea()

matched = match_histograms(image, reference, channel_axis=-1)

fig, (ax1, ax2, ax3) = plt.subplots(
    nrows=1, ncols=3, figsize=(8, 3), sharex=True, sharey=True
)
for aa in (ax1, ax2, ax3):
    aa.set_axis_off()

ax1.imshow(image)
ax1.set_title('Source')
ax2.imshow(reference)
ax2.set_title('Reference')
ax3.imshow(matched)
ax3.set_title('Matched')

plt.tight_layout()
plt.show()


To illustrate the effect of the histogram matching, we plot for each
RGB channel, the histogram and the cumulative histogram. Clearly,
the matched image has the same cumulative histogram as the reference
image for each channel.


fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(8, 8))


for i, img in enumerate((image, reference, matched)):
    for c, c_color in enumerate(('red', 'green', 'blue')):
        img_hist, bins = exposure.histogram(img[..., c], source_range='dtype')
        axes[c, i].plot(bins, img_hist / img_hist.max())
        img_cdf, bins = exposure.cumulative_distribution(img[..., c])
        axes[c, i].plot(bins, img_cdf)
        axes[c, 0].set_ylabel(c_color)

axes[0, 0].set_title('Source')
axes[0, 1].set_title('Reference')
axes[0, 2].set_title('Matched')

plt.tight_layout()
plt.show()


Total running time of the script: (0 minutes 1.123 seconds)


Download Jupyter notebook: plot_histogram_matching.ipynb


Download Python source code: plot_histogram_matching.py


Download zipped: plot_histogram_matching.zip


Gallery generated by Sphinx-Gallery


                

              
              
              
              
              
            

            
            
              
                
                


  
  
    
This Page

    
      
Show Source
    
   


              
            
          

          
            
          
        
      
    

  

  
  
  


  

  
    
      
        

  

    
      © Copyright 2013-2025, the scikit-image team.
      

    
  


      
    

  
  
  
    
      
        

  

    Created using Sphinx 8.2.3.
    

  


      
        


  
  Built with the PyData Sphinx Theme 0.16.1.
