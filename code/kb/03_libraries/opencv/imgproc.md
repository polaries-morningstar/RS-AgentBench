# OpenCV Image Processing: Thresholding & Morphology

Source: https://raw.githubusercontent.com/opencv/opencv/4.x/doc/py_tutorials/py_imgproc/py_thresholding/py_thresholding.markdown

Image Thresholding {#tutorial_py_thresholding}
==================

Goal
----

-   In this tutorial, you will learn simple thresholding, adaptive thresholding and Otsu's thresholding.
-   You will learn the functions **cv.threshold** and **cv.adaptiveThreshold**.

Simple Thresholding
-------------------

Here, the matter is straight-forward. For every pixel, the same threshold value is applied.
If the pixel value is smaller than or equal to the threshold, it is set to 0, otherwise it is set to a maximum value.
The function **cv.threshold** is used to apply the thresholding.
The first argument is the source image, which **should be a grayscale image**.
The second argument is the threshold value which is used to classify the pixel values.
The third argument is the maximum value which is assigned to pixel values exceeding the threshold.
OpenCV provides different types of thresholding which is given by the fourth parameter of the function.
Basic thresholding as described above is done by using the type cv.THRESH_BINARY.
All simple thresholding types are:

-   cv.THRESH_BINARY
-   cv.THRESH_BINARY_INV
-   cv.THRESH_TRUNC
-   cv.THRESH_TOZERO
-   cv.THRESH_TOZERO_INV

See the documentation of the types for the differences.

The method returns two outputs.
The first is the threshold that was used and the second output is the **thresholded image**.

This code compares the different simple thresholding types:
@code{.py}
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread('gradient.png', cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"
ret,thresh1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
ret,thresh2 = cv.threshold(img,127,255,cv.THRESH_BINARY_INV)
ret,thresh3 = cv.threshold(img,127,255,cv.THRESH_TRUNC)
ret,thresh4 = cv.threshold(img,127,255,cv.THRESH_TOZERO)
ret,thresh5 = cv.threshold(img,127,255,cv.THRESH_TOZERO_INV)

titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]

for i in range(6):
    plt.subplot(2,3,i+1),plt.imshow(images[i],'gray',vmin=0,vmax=255)
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])

plt.show()
@endcode
@note To plot multiple images, we have used the plt.subplot() function. Please checkout the matplotlib docs for more details.

The code yields this result:

![image](images/threshold.jpg)

Adaptive Thresholding
---------------------

In the previous section, we used one global value as a threshold.
But this might not be good in all cases, e.g. if an image has different lighting conditions in different areas.
In that case, adaptive thresholding can help.
Here, the algorithm determines the threshold for a pixel based on a small region around it.
So we get different thresholds for different regions of the same image which gives better results for images with varying illumination.

In addition to the parameters described above, the method cv.adaptiveThreshold takes three input parameters:

The **adaptiveMethod** decides how the threshold value is calculated:
    -   cv.ADAPTIVE_THRESH_MEAN_C: The threshold value is the mean of the neighbourhood area minus the constant **C**.
    -   cv.ADAPTIVE_THRESH_GAUSSIAN_C: The threshold value is a gaussian-weighted sum of the neighbourhood
        values minus the constant **C**.

The **blockSize** determines the size of the neighbourhood area and **C** is a constant that is subtracted from the mean or weighted sum of the neighbourhood pixels.

The code below compares global thresholding and adaptive thresholding for an image with varying
illumination:
@code{.py}
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread('sudoku.png', cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"
img = cv.medianBlur(img,5)

ret,th1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
th2 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_MEAN_C,\
            cv.THRESH_BINARY,11,2)
th3 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv.THRESH_BINARY,11,2)

titles = ['Original Image', 'Global Thresholding (v = 127)',
            'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
images = [img, th1, th2, th3]

for i in range(4):
    plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()
@endcode
Result:

![image](images/ada_threshold.jpg)

Otsu's Binarization
-------------------

In global thresholding, we used an arbitrary chosen value as a threshold.
In contrast, Otsu's method avoids having to choose a value and determines it automatically.

Consider an image with only two distinct image values (*bimodal image*), where the histogram would only consist of two peaks.
A good threshold would be in the middle of those two values.
Similarly, Otsu's method determines an optimal global threshold value from the image histogram.

In order to do so, the cv.threshold() function is used, where cv.THRESH_OTSU is passed as an extra flag.
The threshold value can be chosen arbitrary.
The algorithm then finds the optimal threshold value which is returned as the first output.

Check out the example below.
The input image is a noisy image.
In the first case, global thresholding with a value of 127 is applied.
In the second case, Otsu's thresholding is applied directly.
In the third case, the image is first filtered with a 5x5 gaussian kernel to remove the noise, then Otsu thresholding is applied.
See how noise filtering improves the result.
@code{.py}
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread('noisy2.png', cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"

# global thresholding
ret1,th1 = cv.threshold(img,127,255,cv.THRESH_BINARY)

# Otsu's thresholding
ret2,th2 = cv.threshold(img,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)

# Otsu's thresholding after Gaussian filtering
blur = cv.GaussianBlur(img,(5,5),0)
ret3,th3 = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)

# plot all the images and their histograms
images = [img, 0, th1,
          img, 0, th2,
          blur, 0, th3]
titles = ['Original Noisy Image','Histogram','Global Thresholding (v=127)',
          'Original Noisy Image','Histogram',"Otsu's Thresholding",
          'Gaussian filtered Image','Histogram',"Otsu's Thresholding"]

for i in range(3):
    plt.subplot(3,3,i*3+1),plt.imshow(images[i*3],'gray')
    plt.title(titles[i*3]), plt.xticks([]), plt.yticks([])
    plt.subplot(3,3,i*3+2),plt.hist(images[i*3].ravel(),256)
    plt.title(titles[i*3+1]), plt.xticks([]), plt.yticks([])
    plt.subplot(3,3,i*3+3),plt.imshow(images[i*3+2],'gray')
    plt.title(titles[i*3+2]), plt.xticks([]), plt.yticks([])
plt.show()
@endcode
Result:

![image](images/otsu.jpg)

### How does Otsu's Binarization work?

This section demonstrates a Python implementation of Otsu's binarization to show how it actually
works. If you are not interested, you can skip this.

Since we are working with bimodal images, Otsu's algorithm tries to find a threshold value (t) which
minimizes the **weighted within-class variance** given by the relation:

\f[\sigma_w^2(t) = q_1(t)\sigma_1^2(t)+q_2(t)\sigma_2^2(t)\f]

where

\f[q_1(t) = \sum_{i=1}^{t} P(i) \quad \& \quad q_2(t) = \sum_{i=t+1}^{I} P(i)\f]\f[\mu_1(t) = \sum_{i=1}^{t} \frac{iP(i)}{q_1(t)} \quad \& \quad \mu_2(t) = \sum_{i=t+1}^{I} \frac{iP(i)}{q_2(t)}\f]\f[\sigma_1^2(t) = \sum_{i=1}^{t} [i-\mu_1(t)]^2 \frac{P(i)}{q_1(t)} \quad \& \quad \sigma_2^2(t) = \sum_{i=t+1}^{I} [i-\mu_2(t)]^2 \frac{P(i)}{q_2(t)}\f]

It actually finds a value of t which lies in between two peaks such that variances to both classes
are minimal. It can be simply implemented in Python as follows:
@code{.py}
img = cv.imread('noisy2.png', cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"
blur = cv.GaussianBlur(img,(5,5),0)

# find normalized_histogram, and its cumulative distribution function
hist = cv.calcHist([blur],[0],None,[256],[0,256])
hist_norm = hist.ravel()/hist.sum()
Q = hist_norm.cumsum()

bins = np.arange(256)

fn_min = np.inf
thresh = -1

for i in range(1,256):
    p1,p2 = np.hsplit(hist_norm,[i]) # probabilities
    q1,q2 = Q[i],Q[255]-Q[i] # cum sum of classes
    if q1 < 1.e-6 or q2 < 1.e-6:
        continue
    b1,b2 = np.hsplit(bins,[i]) # weights

    # finding means and variances
    m1,m2 = np.sum(p1*b1)/q1, np.sum(p2*b2)/q2
    v1,v2 = np.sum(((b1-m1)**2)*p1)/q1,np.sum(((b2-m2)**2)*p2)/q2

    # calculates the minimization function
    fn = v1*q1 + v2*q2
    if fn < fn_min:
        fn_min = fn
        thresh = i

# find otsu's threshold value with OpenCV function
ret, otsu = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
print( "{} {}".format(thresh,ret) )
@endcode

Additional Resources
--------------------

-#  Digital Image Processing, Rafael C. Gonzalez

Exercises
---------

-#  There are some optimizations available for Otsu's binarization. You can search and implement it.

---
Source: https://raw.githubusercontent.com/opencv/opencv/4.x/doc/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.markdown

Morphological Transformations {#tutorial_py_morphological_ops}
=============================

Goal
----

In this chapter,
    -   We will learn different morphological operations like Erosion, Dilation, Opening, Closing
        etc.
    -   We will see different functions like : **cv.erode()**, **cv.dilate()**,
        **cv.morphologyEx()** etc.

Theory
------

Morphological transformations are some simple operations based on the image shape. It is normally
performed on binary images. It needs two inputs, one is our original image, second one is called
**structuring element** or **kernel** which decides the nature of operation. Two basic morphological
operators are Erosion and Dilation. Then its variant forms like Opening, Closing, Gradient etc also
comes into play. We will see them one-by-one with help of following image:

![image](images/j.png)

### 1. Erosion

The basic idea of erosion is just like soil erosion only, it erodes away the boundaries of
foreground object (Always try to keep foreground in white). So what it does? The kernel slides
through the image (as in 2D convolution). A pixel in the original image (either 1 or 0) will be
considered 1 only if all the pixels under the kernel is 1, otherwise it is eroded (made to zero).

So what happends is that, all the pixels near boundary will be discarded depending upon the size of
kernel. So the thickness or size of the foreground object decreases or simply white region decreases
in the image. It is useful for removing small white noises (as we have seen in colorspace chapter),
detach two connected objects etc.

Here, as an example, I would use a 5x5 kernel with full of ones. Let's see it how it works:
@code{.py}
import cv2 as cv
import numpy as np

img = cv.imread('j.png', cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"
kernel = np.ones((5,5),np.uint8)
erosion = cv.erode(img,kernel,iterations = 1)
@endcode
Result:

![image](images/erosion.png)

### 2. Dilation

It is just opposite of erosion. Here, a pixel element is '1' if at least one pixel under the kernel
is '1'. So it increases the white region in the image or size of foreground object increases.
Normally, in cases like noise removal, erosion is followed by dilation. Because, erosion removes
white noises, but it also shrinks our object. So we dilate it. Since noise is gone, they won't come
back, but our object area increases. It is also useful in joining broken parts of an object.
@code{.py}
dilation = cv.dilate(img,kernel,iterations = 1)
@endcode
Result:

![image](images/dilation.png)

### 3. Opening

Opening is just another name of **erosion followed by dilation**. It is useful in removing noise, as
we explained above. Here we use the function, **cv.morphologyEx()**
@code{.py}
opening = cv.morphologyEx(img, cv.MORPH_OPEN, kernel)
@endcode
Result:

![image](images/opening.png)

### 4. Closing

Closing is reverse of Opening, **Dilation followed by Erosion**. It is useful in closing small holes
inside the foreground objects, or small black points on the object.
@code{.py}
closing = cv.morphologyEx(img, cv.MORPH_CLOSE, kernel)
@endcode
Result:

![image](images/closing.png)

### 5. Morphological Gradient

It is the difference between dilation and erosion of an image.

The result will look like the outline of the object.
@code{.py}
gradient = cv.morphologyEx(img, cv.MORPH_GRADIENT, kernel)
@endcode
Result:

![image](images/gradient.png)

### 6. Top Hat

It is the difference between input image and Opening of the image. Below example is done for a 9x9
kernel.
@code{.py}
tophat = cv.morphologyEx(img, cv.MORPH_TOPHAT, kernel)
@endcode
Result:

![image](images/tophat.png)

### 7. Black Hat

It is the difference between the closing of the input image and input image.
@code{.py}
blackhat = cv.morphologyEx(img, cv.MORPH_BLACKHAT, kernel)
@endcode
Result:

![image](images/blackhat.png)

Structuring Element
-------------------

We manually created a structuring elements in the previous examples with help of Numpy. It is
rectangular shape. But in some cases, you may need elliptical/circular shaped kernels. So for this
purpose, OpenCV has a function, **cv.getStructuringElement()**. You just pass the shape and size of
the kernel, you get the desired kernel.
@code{.py}
# Rectangular Kernel
>>> cv.getStructuringElement(cv.MORPH_RECT,(5,5))
array([[1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1]], dtype=uint8)

# Elliptical Kernel
>>> cv.getStructuringElement(cv.MORPH_ELLIPSE,(5,5))
array([[0, 0, 1, 0, 0],
       [1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1],
       [0, 0, 1, 0, 0]], dtype=uint8)

# Cross-shaped Kernel
>>> cv.getStructuringElement(cv.MORPH_CROSS,(5,5))
array([[0, 0, 1, 0, 0],
       [0, 0, 1, 0, 0],
       [1, 1, 1, 1, 1],
       [0, 0, 1, 0, 0],
       [0, 0, 1, 0, 0]], dtype=uint8)

# Diamond-shaped Kernel
>>> cv.getStructuringElement(cv.MORPH_DIAMOND,(5,5))
array([[0, 0, 1, 0, 0],
       [0, 1, 1, 1, 0],
       [1, 1, 1, 1, 1],
       [0, 1, 1, 1, 0],
       [0, 0, 1, 0, 0]], dtype=uint8)
@endcode
Additional Resources
--------------------

-#  [Morphological Operations](http://homepages.inf.ed.ac.uk/rbf/HIPR2/morops.htm) at HIPR2

---
Source: https://raw.githubusercontent.com/opencv/opencv/4.x/doc/py_tutorials/py_imgproc/py_gradients/py_gradients.markdown

Image Gradients {#tutorial_py_gradients}
===============

Goal
----

In this chapter, we will learn to:

-   Find Image gradients, edges etc
-   We will see following functions : **cv.Sobel()**, **cv.Scharr()**, **cv.Laplacian()** etc

Theory
------

OpenCV provides three types of gradient filters or High-pass filters, Sobel, Scharr and Laplacian.
We will see each one of them.

### 1. Sobel and Scharr Derivatives

Sobel operators is a joint Gaussian smoothing plus differentiation operation, so it is more
resistant to noise. You can specify the direction of derivatives to be taken, vertical or horizontal
(by the arguments, yorder and xorder respectively). You can also specify the size of kernel by the
argument ksize. If ksize = -1, a 3x3 Scharr filter is used which gives better results than 3x3 Sobel
filter. Please see the docs for kernels used.

### 2. Laplacian Derivatives

It calculates the Laplacian of the image given by the relation,
\f$\Delta src = \frac{\partial ^2{src}}{\partial x^2} + \frac{\partial ^2{src}}{\partial y^2}\f$ where
each derivative is found using Sobel derivatives. If ksize = 1, then following kernel is used for
filtering:

\f[kernel = \begin{bmatrix} 0 & 1 & 0 \\ 1 & -4 & 1 \\ 0 & 1 & 0  \end{bmatrix}\f]

Code
----

Below code shows all operators in a single diagram. All kernels are of 5x5 size. Depth of output
image is passed -1 to get the result in np.uint8 type.
@code{.py}
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

img = cv.imread('dave.jpg', cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"

laplacian = cv.Laplacian(img,cv.CV_64F)
sobelx = cv.Sobel(img,cv.CV_64F,1,0,ksize=5)
sobely = cv.Sobel(img,cv.CV_64F,0,1,ksize=5)

plt.subplot(2,2,1),plt.imshow(img,cmap = 'gray')
plt.title('Original'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,2),plt.imshow(laplacian,cmap = 'gray')
plt.title('Laplacian'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,3),plt.imshow(sobelx,cmap = 'gray')
plt.title('Sobel X'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,4),plt.imshow(sobely,cmap = 'gray')
plt.title('Sobel Y'), plt.xticks([]), plt.yticks([])

plt.show()
@endcode
Result:

![image](images/gradients.jpg)

One Important Matter!
---------------------

In our last example, output datatype is cv.CV_8U or np.uint8. But there is a slight problem with
that. Black-to-White transition is taken as Positive slope (it has a positive value) while
White-to-Black transition is taken as a Negative slope (It has negative value). So when you convert
data to np.uint8, all negative slopes are made zero. In simple words, you miss that edge.

If you want to detect both edges, better option is to keep the output datatype to some higher forms,
like cv.CV_16S, cv.CV_64F etc, take its absolute value and then convert back to cv.CV_8U.
Below code demonstrates this procedure for a horizontal Sobel filter and difference in results.
@code{.py}
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

img = cv.imread('box.png', cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"

# Output dtype = cv.CV_8U
sobelx8u = cv.Sobel(img,cv.CV_8U,1,0,ksize=5)

# Output dtype = cv.CV_64F. Then take its absolute and convert to cv.CV_8U
sobelx64f = cv.Sobel(img,cv.CV_64F,1,0,ksize=5)
abs_sobel64f = np.absolute(sobelx64f)
sobel_8u = np.uint8(abs_sobel64f)

plt.subplot(1,3,1),plt.imshow(img,cmap = 'gray')
plt.title('Original'), plt.xticks([]), plt.yticks([])
plt.subplot(1,3,2),plt.imshow(sobelx8u,cmap = 'gray')
plt.title('Sobel CV_8U'), plt.xticks([]), plt.yticks([])
plt.subplot(1,3,3),plt.imshow(sobel_8u,cmap = 'gray')
plt.title('Sobel abs(CV_64F)'), plt.xticks([]), plt.yticks([])

plt.show()
@endcode
Check the result below:

![image](images/double_edge.jpg)

---
Source: https://raw.githubusercontent.com/opencv/opencv/4.x/doc/py_tutorials/py_imgproc/py_canny/py_canny.markdown

Canny Edge Detection {#tutorial_py_canny}
====================

Goal
----

In this chapter, we will learn about

-   Concept of Canny edge detection
-   OpenCV functions for that : **cv.Canny()**

Theory
------

Canny Edge Detection is a popular edge detection algorithm. It was developed by John F. Canny in
1986. It is a multi-stage algorithm and we will go through each stages.

-#  **Noise Reduction**

    Since edge detection is susceptible to noise in the image, first step is to remove the noise in the
    image with a 5x5 Gaussian filter. We have already seen this in previous chapters.

-#  **Finding Intensity Gradient of the Image**

    Smoothened image is then filtered with a Sobel kernel in both horizontal and vertical direction to
    get first derivative in horizontal direction (\f$G_x\f$) and vertical direction (\f$G_y\f$). From these two
    images, we can find edge gradient and direction for each pixel as follows:

    \f[
    Edge\_Gradient \; (G) = \sqrt{G_x^2 + G_y^2} \\
    Angle \; (\theta) = \tan^{-1} \bigg(\frac{G_y}{G_x}\bigg)
    \f]

    Gradient direction is always perpendicular to edges. It is rounded to one of four angles
    representing vertical, horizontal and two diagonal directions.

-#  **Non-maximum Suppression**

    After getting gradient magnitude and direction, a full scan of image is done to remove any unwanted
    pixels which may not constitute the edge. For this, at every pixel, pixel is checked if it is a
    local maximum in its neighborhood in the direction of gradient. Check the image below:

    ![image](images/nms.jpg)

    Point A is on the edge ( in vertical direction). Gradient direction is normal to the edge. Point B
    and C are in gradient directions. So point A is checked with point B and C to see if it forms a
    local maximum. If so, it is considered for next stage, otherwise, it is suppressed ( put to zero).

    In short, the result you get is a binary image with "thin edges".

-#  **Hysteresis Thresholding**

    This stage decides which are all edges are really edges and which are not. For this, we need two
    threshold values, minVal and maxVal. Any edges with intensity gradient more than maxVal are sure to
    be edges and those below minVal are sure to be non-edges, so discarded. Those who lie between these
    two thresholds are classified edges or non-edges based on their connectivity. If they are connected
    to "sure-edge" pixels, they are considered to be part of edges. Otherwise, they are also discarded.
    See the image below:

    ![image](images/hysteresis.jpg)

    The edge A is above the maxVal, so considered as "sure-edge". Although edge C is below maxVal, it is
    connected to edge A, so that also considered as valid edge and we get that full curve. But edge B,
    although it is above minVal and is in same region as that of edge C, it is not connected to any
    "sure-edge", so that is discarded. So it is very important that we have to select minVal and maxVal
    accordingly to get the correct result.

    This stage also removes small pixels noises on the assumption that edges are long lines.

So what we finally get is strong edges in the image.

Canny Edge Detection in OpenCV
------------------------------

OpenCV puts all the above in single function, **cv.Canny()**. We will see how to use it. First
argument is our input image. Second and third arguments are our minVal and maxVal respectively.
Fourth argument is aperture_size. It is the size of Sobel kernel used for find image gradients. By
default it is 3. Last argument is L2gradient which specifies the equation for finding gradient
magnitude. If it is True, it uses the equation mentioned above which is more accurate, otherwise it
uses this function: \f$Edge\_Gradient \; (G) = |G_x| + |G_y|\f$. By default, it is False.
@code{.py}
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

img = cv.imread('messi5.jpg', cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"
edges = cv.Canny(img,100,200)

plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()
@endcode
See the result below:

![image](images/canny1.jpg)

Additional Resources
--------------------

-#  Canny edge detector at [Wikipedia](http://en.wikipedia.org/wiki/Canny_edge_detector)
-#  [Canny Edge Detection Tutorial](http://dasl.unlv.edu/daslDrexel/alumni/bGreen/www.pages.drexel.edu/_weg22/can_tut.html) by
    Bill Green, 2002.

Exercises
---------

-#  Write a small application to find the Canny edge detection whose threshold values can be varied
    using two trackbars. This way, you can understand the effect of threshold values.

---
Source: https://raw.githubusercontent.com/opencv/opencv/4.x/doc/py_tutorials/py_imgproc/py_contours/py_contours_begin/py_contours_begin.markdown

Contours : Getting Started {#tutorial_py_contours_begin}
==========================

@next_tutorial{tutorial_py_contour_features}

Goal
----

-   Understand what contours are.
-   Learn to find contours, draw contours etc
-   You will see these functions : **cv.findContours()**, **cv.drawContours()**

What are contours?
------------------

Contours can be explained simply as a curve joining all the continuous points (along the boundary),
having same color or intensity. The contours are a useful tool for shape analysis and object
detection and recognition.

-   For better accuracy, use binary images. So before finding contours, apply threshold or canny
    edge detection.
-   Since OpenCV 3.2, findContours() no longer modifies the source image.
-   In OpenCV, finding contours is like finding white object from black background. So remember,
    object to be found should be white and background should be black.

Let's see how to find contours of a binary image:
@code{.py}
import numpy as np
import cv2 as cv

im = cv.imread('test.jpg')
assert im is not None, "file could not be read, check with os.path.exists()"
imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(imgray, 127, 255, 0)
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
@endcode
See, there are three arguments in **cv.findContours()** function, first one is source image, second
is contour retrieval mode, third is contour approximation method. And it outputs the contours and hierarchy.
Contours is a Python list of all the contours in the image. Each individual contour is a
Numpy array of (x,y) coordinates of boundary points of the object.

@note We will discuss second and third arguments and about hierarchy in details later. Until then,
the values given to them in code sample will work fine for all images.

How to draw the contours?
-------------------------

To draw the contours, cv.drawContours function is used. It can also be used to draw any shape
provided you have its boundary points. Its first argument is source image, second argument is the
contours which should be passed as a Python list, third argument is index of contours (useful when
drawing individual contour. To draw all contours, pass -1) and remaining arguments are color,
thickness etc.

* To draw all the contours in an image:
@code{.py}
cv.drawContours(img, contours, -1, (0,255,0), 3)
@endcode
* To draw an individual contour, say 4th contour:
@code{.py}
cv.drawContours(img, contours, 3, (0,255,0), 3)
@endcode
* But most of the time, below method will be useful:
@code{.py}
cnt = contours[4]
cv.drawContours(img, [cnt], 0, (0,255,0), 3)
@endcode

@note Last two methods are same, but when you go forward, you will see last one is more useful.

Contour Approximation Method
============================

This is the third argument in cv.findContours function. What does it denote actually?

Above, we told that contours are the boundaries of a shape with same intensity. It stores the (x,y)
coordinates of the boundary of a shape. But does it store all the coordinates ? That is specified by
this contour approximation method.

If you pass cv.CHAIN_APPROX_NONE, all the boundary points are stored. But actually do we need all
the points? For eg, you found the contour of a straight line. Do you need all the points on the line
to represent that line? No, we need just two end points of that line. This is what
cv.CHAIN_APPROX_SIMPLE does. It removes all redundant points and compresses the contour, thereby
saving memory.

Below image of a rectangle demonstrate this technique. Just draw a circle on all the coordinates in
the contour array (drawn in blue color). First image shows points I got with cv.CHAIN_APPROX_NONE
(734 points) and second image shows the one with cv.CHAIN_APPROX_SIMPLE (only 4 points). See, how
much memory it saves!!!

![image](images/none.jpg)

---
Source: https://raw.githubusercontent.com/opencv/opencv/4.x/doc/py_tutorials/py_imgproc/py_contours/py_contour_features/py_contour_features.markdown

Contour Features {#tutorial_py_contour_features}
================

@prev_tutorial{tutorial_py_contours_begin}
@next_tutorial{tutorial_py_contour_properties}

Goal
----

In this article, we will learn

-   To find the different features of contours, like area, perimeter, centroid, bounding box etc
-   You will see plenty of functions related to contours.

1. Moments
----------

Image moments help you to calculate some features like center of mass of the object, area of the
object etc. Check out the wikipedia page on [Image
Moments](http://en.wikipedia.org/wiki/Image_moment)

The function **cv.moments()** gives a dictionary of all moment values calculated. See below:
@code{.py}
import numpy as np
import cv2 as cv

img = cv.imread('star.jpg', cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"
ret,thresh = cv.threshold(img,127,255,0)
contours,hierarchy = cv.findContours(thresh, 1, 2)

cnt = contours[0]
M = cv.moments(cnt)
print( M )
@endcode
From this moments, you can extract useful data like area, centroid etc. Centroid is given by the
relations, \f$C_x = \frac{M_{10}}{M_{00}}\f$ and \f$C_y = \frac{M_{01}}{M_{00}}\f$. This can be done as
follows:
@code{.py}
cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])
@endcode

2. Contour Area
---------------

Contour area is given by the function **cv.contourArea()** or from moments, **M['m00']**.
@code{.py}
area = cv.contourArea(cnt)
@endcode

3. Contour Perimeter
--------------------

It is also called arc length. It can be found out using **cv.arcLength()** function. Second
argument specify whether shape is a closed contour (if passed True), or just a curve.
@code{.py}
perimeter = cv.arcLength(cnt,True)
@endcode

4. Contour Approximation
------------------------

It approximates a contour shape to another shape with less number of vertices depending upon the
precision we specify. It is an implementation of [Douglas-Peucker
algorithm](http://en.wikipedia.org/wiki/Ramer-Douglas-Peucker_algorithm). Check the wikipedia page
for algorithm and demonstration.

To understand this, suppose you are trying to find a square in an image, but due to some problems in
the image, you didn't get a perfect square, but a "bad shape" (As shown in first image below). Now
you can use this function to approximate the shape. In this, second argument is called epsilon,
which is maximum distance from contour to approximated contour. It is an accuracy parameter. A wise
selection of epsilon is needed to get the correct output.
@code{.py}
epsilon = 0.1*cv.arcLength(cnt,True)
approx = cv.approxPolyDP(cnt,epsilon,True)
@endcode
Below, in second image, green line shows the approximated curve for epsilon = 10% of arc length.
Third image shows the same for epsilon = 1% of the arc length. Third argument specifies whether
curve is closed or not.

![image](images/approx.jpg)

5. Convex Hull
--------------

Convex Hull will look similar to contour approximation, but it is not (Both may provide same results
in some cases). Here, **cv.convexHull()** function checks a curve for convexity defects and
corrects it. Generally speaking, convex curves are the curves which are always bulged out, or
at-least flat. And if it is bulged inside, it is called convexity defects. For example, check the
below image of hand. Red line shows the convex hull of hand. The double-sided arrow marks shows the
convexity defects, which are the local maximum deviations of hull from contours.

![image](images/convexitydefects.jpg)

There is a little bit things to discuss about it its syntax:
@code{.py}
hull = cv.convexHull(points[, hull[, clockwise[, returnPoints]]])
@endcode
Arguments details:

-   **points** are the contours we pass into.
-   **hull** is the output, normally we avoid it.
-   **clockwise** : Orientation flag. If it is True, the output convex hull is oriented clockwise.
    Otherwise, it is oriented counter-clockwise.
-   **returnPoints** : By default, True. Then it returns the coordinates of the hull points. If
    False, it returns the indices of contour points corresponding to the hull points.

So to get a convex hull as in above image, following is sufficient:
@code{.py}
hull = cv.convexHull(cnt)
@endcode
But if you want to find convexity defects, you need to pass returnPoints = False. To understand it,
we will take the rectangle image above. First I found its contour as cnt. Now I found its convex
hull with returnPoints = True, I got following values:
[[[234 202]], [[ 51 202]], [[ 51 79]], [[234 79]]] which are the four corner points of rectangle.
Now if do the same with returnPoints = False, I get following result: [[129],[ 67],[ 0],[142]].
These are the indices of corresponding points in contours. For eg, check the first value:
cnt[129] = [[234, 202]] which is same as first result (and so on for others).

You will see it again when we discuss about convexity defects.

6. Checking Convexity
---------------------

There is a function to check if a curve is convex or not, **cv.isContourConvex()**. It just return
whether True or False. Not a big deal.
@code{.py}
k = cv.isContourConvex(cnt)
@endcode

7. Bounding Rectangle
---------------------

There are two types of bounding rectangles.

### 7.a. Straight Bounding Rectangle

It is a straight rectangle, it doesn't consider the rotation of the object. So area of the bounding
rectangle won't be minimum. It is found by the function **cv.boundingRect()**.

Let (x,y) be the top-left coordinate of the rectangle and (w,h) be its width and height.
@code{.py}
x,y,w,h = cv.boundingRect(cnt)
cv.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
@endcode

### 7.b. Rotated Rectangle

Here, bounding rectangle is drawn with minimum area, so it considers the rotation also. The function
used is **cv.minAreaRect()**. It returns a Box2D structure which contains following details - (
center (x,y), (width, height), angle of rotation ). But to draw this rectangle, we need 4 corners of
the rectangle. It is obtained by the function **cv.boxPoints()**
@code{.py}
rect = cv.minAreaRect(cnt)
box = cv.boxPoints(rect)
box = np.int0(box)
cv.drawContours(img,[box],0,(0,0,255),2)
@endcode
Both the rectangles are shown in a single image. Green rectangle shows the normal bounding rect. Red
rectangle is the rotated rect.

![image](images/boundingrect.png)

8. Minimum Enclosing Circle
---------------------------

Next we find the circumcircle of an object using the function **cv.minEnclosingCircle()**. It is a
circle which completely covers the object with minimum area.
@code{.py}
(x,y),radius = cv.minEnclosingCircle(cnt)
center = (int(x),int(y))
radius = int(radius)
cv.circle(img,center,radius,(0,255,0),2)
@endcode
![image](images/circumcircle.png)

9. Fitting an Ellipse
---------------------

Next one is to fit an ellipse to an object. It returns the rotated rectangle in which the ellipse is
inscribed.
@code{.py}
ellipse = cv.fitEllipse(cnt)
cv.ellipse(img,ellipse,(0,255,0),2)
@endcode
![image](images/fitellipse.png)

10. Fitting a Line
------------------

Similarly we can fit a line to a set of points. Below image contains a set of white points. We can
approximate a straight line to it.
@code{.py}
rows,cols = img.shape[:2]
[vx,vy,x,y] = cv.fitLine(cnt, cv.DIST_L2,0,0.01,0.01)
lefty = int((-x*vy/vx) + y)
righty = int(((cols-x)*vy/vx)+y)
cv.line(img,(cols-1,righty),(0,lefty),(0,255,0),2)
@endcode
![image](images/fitline.jpg)

---
Source: https://raw.githubusercontent.com/opencv/opencv/4.x/doc/py_tutorials/py_imgproc/py_contours/py_contour_properties/py_contour_properties.markdown

Contour Properties {#tutorial_py_contour_properties}
==================

@prev_tutorial{tutorial_py_contour_features}
@next_tutorial{tutorial_py_contours_more_functions}

Here we will learn to extract some frequently used properties of objects like Solidity, Equivalent
Diameter, Mask image, Mean Intensity etc. More features can be found at [Matlab regionprops
documentation](http://www.mathworks.in/help/images/ref/regionprops.html).

*(NB : Centroid, Area, Perimeter etc also belong to this category, but we have seen it in last
chapter)*

1. Aspect Ratio
---------------

It is the ratio of width to height of bounding rect of the object.

\f[Aspect \; Ratio = \frac{Width}{Height}\f]
@code{.py}
x,y,w,h = cv.boundingRect(cnt)
aspect_ratio = float(w)/h
@endcode

2. Extent
---------

Extent is the ratio of contour area to bounding rectangle area.

\f[Extent = \frac{Object \; Area}{Bounding \; Rectangle \; Area}\f]
@code{.py}
area = cv.contourArea(cnt)
x,y,w,h = cv.boundingRect(cnt)
rect_area = w*h
extent = float(area)/rect_area
@endcode

3. Solidity
-----------

Solidity is the ratio of contour area to its convex hull area.

\f[Solidity = \frac{Contour \; Area}{Convex \; Hull \; Area}\f]
@code{.py}
area = cv.contourArea(cnt)
hull = cv.convexHull(cnt)
hull_area = cv.contourArea(hull)
solidity = float(area)/hull_area
@endcode

4. Equivalent Diameter
----------------------

Equivalent Diameter is the diameter of the circle whose area is same as the contour area.

\f[Equivalent \; Diameter = \sqrt{\frac{4 \times Contour \; Area}{\pi}}\f]
@code{.py}
area = cv.contourArea(cnt)
equi_diameter = np.sqrt(4*area/np.pi)
@endcode

5. Orientation
--------------

Orientation is the angle at which object is directed. Following method also gives the Major Axis and
Minor Axis lengths.
@code{.py}
(x,y),(MA,ma),angle = cv.fitEllipse(cnt)
@endcode

6. Mask and Pixel Points
------------------------

In some cases, we may need all the points which comprises that object. It can be done as follows:
@code{.py}
mask = np.zeros(imgray.shape,np.uint8)
cv.drawContours(mask,[cnt],0,255,-1)
pixelpoints = np.transpose(np.nonzero(mask))
#pixelpoints = cv.findNonZero(mask)
@endcode
Here, two methods, one using Numpy functions, next one using OpenCV function (last commented line)
are given to do the same. Results are also same, but with a slight difference. Numpy gives
coordinates in **(row, column)** format, while OpenCV gives coordinates in **(x,y)** format. So
basically the answers will be interchanged. Note that, **row = y** and **column = x**.

7. Maximum Value, Minimum Value and their locations
---------------------------------------------------

We can find these parameters using a mask image.
@code{.py}
min_val, max_val, min_loc, max_loc = cv.minMaxLoc(imgray,mask = mask)
@endcode

8. Mean Color or Mean Intensity
-------------------------------

Here, we can find the average color of an object. Or it can be average intensity of the object in
grayscale mode. We again use the same mask to do it.
@code{.py}
mean_val = cv.mean(im,mask = mask)
@endcode

9. Extreme Points
-----------------

Extreme Points means topmost, bottommost, rightmost and leftmost points of the object.
@code{.py}
leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])
@endcode
For eg, if I apply it to an Indian map, I get the following result :

![image](images/extremepoints.jpg)

Exercises
---------

-#  There are still some features left in matlab regionprops doc. Try to implement them.

---
Source: https://raw.githubusercontent.com/opencv/opencv/4.x/doc/py_tutorials/py_imgproc/py_histograms/py_histogram_begins/py_histogram_begins.markdown

Histograms - 1 : Find, Plot, Analyze !!! {#tutorial_py_histogram_begins}
========================================

Goal
----

Learn to
    -   Find histograms, using both OpenCV and Numpy functions
    -   Plot histograms, using OpenCV and Matplotlib functions
    -   You will see these functions : **cv.calcHist()**, **np.histogram()** etc.

Theory
------

So what is histogram ? You can consider histogram as a graph or plot, which gives you an overall
idea about the intensity distribution of an image. It is a plot with pixel values (ranging from 0 to
255, not always) in X-axis and corresponding number of pixels in the image on Y-axis.

It is just another way of understanding the image. By looking at the histogram of an image, you get
intuition about contrast, brightness, intensity distribution etc of that image. Almost all image
processing tools today, provides features on histogram. Below is an image from [Cambridge in Color
website](http://www.cambridgeincolour.com/tutorials/histograms1.htm), and I recommend you to visit
the site for more details.

![image](images/histogram_sample.jpg)

You can see the image and its histogram. (Remember, this histogram is drawn for grayscale image, not
color image). Left region of histogram shows the amount of darker pixels in image and right region
shows the amount of brighter pixels. From the histogram, you can see dark region is more than
brighter region, and amount of midtones (pixel values in mid-range, say around 127) are very less.

Find Histogram
--------------

Now we have an idea on what is histogram, we can look into how to find this. Both OpenCV and Numpy
come with in-built function for this. Before using those functions, we need to understand some
terminologies related with histograms.

**BINS** :The above histogram shows the number of pixels for every pixel value, ie from 0 to 255. ie
you need 256 values to show the above histogram. But consider, what if you need not find the number
of pixels for all pixel values separately, but number of pixels in a interval of pixel values? say
for example, you need to find the number of pixels lying between 0 to 15, then 16 to 31, ..., 240 to 255.
You will need only 16 values to represent the histogram. And that is what is shown in example
given in @ref tutorial_histogram_calculation "OpenCV Tutorials on histograms".

So what you do is simply split the whole histogram to 16 sub-parts and value of each sub-part is the
sum of all pixel count in it. This each sub-part is called "BIN". In first case, number of bins
were 256 (one for each pixel) while in second case, it is only 16. BINS is represented by the term
**histSize** in OpenCV docs.

**DIMS** : It is the number of parameters for which we collect the data. In this case, we collect
data regarding only one thing, intensity value. So here it is 1.

**RANGE** : It is the range of intensity values you want to measure. Normally, it is [0,256], ie all
intensity values.

### 1. Histogram Calculation in OpenCV

So now we use **cv.calcHist()** function to find the histogram. Let's familiarize with the function
and its parameters :

<center><em>cv.calcHist(images, channels, mask, histSize, ranges[, hist[, accumulate]])</em></center>

-#  images : it is the source image of type uint8 or float32. it should be given in square brackets,
    ie, "[img]".
-#  channels : it is also given in square brackets. It is the index of channel for which we
    calculate histogram. For example, if input is grayscale image, its value is [0]. For color
    image, you can pass [0], [1] or [2] to calculate histogram of blue, green or red channel
    respectively.
-#  mask : mask image. To find histogram of full image, it is given as "None". But if you want to
    find histogram of particular region of image, you have to create a mask image for that and give
    it as mask. (I will show an example later.)
-#  histSize : this represents our BIN count. Need to be given in square brackets. For full scale,
    we pass [256].
-#  ranges : this is our RANGE. Normally, it is [0,256].

So let's start with a sample image. Simply load an image in grayscale mode and find its full
histogram.
@code{.py}
img = cv.imread('home.jpg', cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"
hist = cv.calcHist([img],[0],None,[256],[0,256])
@endcode
hist is a 256x1 array, each value corresponds to number of pixels in that image with its
corresponding pixel value.

### 2. Histogram Calculation in Numpy

Numpy also provides you a function, **np.histogram()**. So instead of calcHist() function, you can
try below line :
@code{.py}
hist,bins = np.histogram(img.ravel(),256,[0,256])
@endcode
hist is same as we calculated before. But bins will have 257 elements, because Numpy calculates bins
as 0-0.99, 1-1.99, 2-2.99 etc. So final range would be 255-255.99. To represent that, they also add
256 at end of bins. But we don't need that 256. Upto 255 is sufficient.

@note Numpy has another function, **np.bincount()** which is much faster than (around 10X)
np.histogram(). So for one-dimensional histograms, you can better try that. Don't forget to set
minlength = 256 in np.bincount. For example, hist = np.bincount(img.ravel(),minlength=256)

@note OpenCV function is faster than (around 40X) than np.histogram(). So stick with OpenCV
function.

Now we should plot histograms, but how?

Plotting Histograms
-------------------

There are two ways for this,
    -#  Short Way : use Matplotlib plotting functions
    -#  Long Way : use OpenCV drawing functions

### 1. Using Matplotlib

Matplotlib comes with a histogram plotting function : matplotlib.pyplot.hist()

It directly finds the histogram and plot it. You need not use calcHist() or np.histogram() function
to find the histogram. See the code below:
@code{.py}
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

img = cv.imread('home.jpg', cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"
plt.hist(img.ravel(),256,[0,256]); plt.show()
@endcode
You will get a plot as below :

![image](images/histogram_matplotlib.jpg)

Or you can use normal plot of matplotlib, which would be good for BGR plot. For that, you need to
find the histogram data first. Try below code:
@code{.py}
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

img = cv.imread('home.jpg')
assert img is not None, "file could not be read, check with os.path.exists()"
color = ('b','g','r')
for i,col in enumerate(color):
    histr = cv.calcHist([img],[i],None,[256],[0,256])
    plt.plot(histr,color = col)
    plt.xlim([0,256])
plt.show()
@endcode
Result:

![image](images/histogram_rgb_plot.jpg)

You can deduct from the above graph that, blue has some high value areas in the image (obviously it
should be due to the sky)

### 2. Using OpenCV

Well, here you adjust the values of histograms along with its bin values to look like x,y
coordinates so that you can draw it using cv.line() or cv.polyline() function to generate same
image as above. This is already available with OpenCV-Python2 official samples. Check the
code at samples/python/hist.py.

Application of Mask
-------------------

We used cv.calcHist() to find the histogram of the full image. What if you want to find histograms
of some regions of an image? Just create a mask image with white color on the region you want to
find histogram and black otherwise. Then pass this as the mask.
@code{.py}
img = cv.imread('home.jpg', cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"

# create a mask
mask = np.zeros(img.shape[:2], np.uint8)
mask[100:300, 100:400] = 255
masked_img = cv.bitwise_and(img,img,mask = mask)

# Calculate histogram with mask and without mask
# Check third argument for mask
hist_full = cv.calcHist([img],[0],None,[256],[0,256])
hist_mask = cv.calcHist([img],[0],mask,[256],[0,256])

plt.subplot(221), plt.imshow(img, 'gray')
plt.subplot(222), plt.imshow(mask,'gray')
plt.subplot(223), plt.imshow(masked_img, 'gray')
plt.subplot(224), plt.plot(hist_full), plt.plot(hist_mask)
plt.xlim([0,256])

plt.show()
@endcode
See the result. In the histogram plot, blue line shows histogram of full image while green line
shows histogram of masked region.

![image](images/histogram_masking.jpg)

Additional Resources
--------------------

-#  [Cambridge in Color website](http://www.cambridgeincolour.com/tutorials/histograms1.htm)

---
Source: https://raw.githubusercontent.com/opencv/opencv/4.x/doc/py_tutorials/py_imgproc/py_histograms/py_histogram_equalization/py_histogram_equalization.markdown

Histograms - 2: Histogram Equalization {#tutorial_py_histogram_equalization}
======================================

Goal
----

In this section,

-   We will learn the concepts of histogram equalization and use it to improve the contrast of our
    images.

Theory
------

Consider an image whose pixel values are confined to some specific range of values only. For eg,
brighter image will have all pixels confined to high values. But a good image will have pixels from
all regions of the image. So you need to stretch this histogram to either ends (as given in below
image, from wikipedia) and that is what Histogram Equalization does (in simple words). This normally
improves the contrast of the image.

![image](images/histogram_equalization.png)

I would recommend you to read the wikipedia page on [Histogram
Equalization](http://en.wikipedia.org/wiki/Histogram_equalization) for more details about it. It has
a very good explanation with worked out examples, so that you would understand almost everything
after reading that. Instead, here we will see its Numpy implementation. After that, we will see
OpenCV function.
@code{.py}
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

img = cv.imread('wiki.jpg', cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"

hist,bins = np.histogram(img.flatten(),256,[0,256])

cdf = hist.cumsum()
cdf_normalized = cdf * float(hist.max()) / cdf.max()

plt.plot(cdf_normalized, color = 'b')
plt.hist(img.flatten(),256,[0,256], color = 'r')
plt.xlim([0,256])
plt.legend(('cdf','histogram'), loc = 'upper left')
plt.show()
@endcode
![image](images/histeq_numpy1.jpg)

You can see histogram lies in brighter region. We need the full spectrum. For that, we need a
transformation function which maps the input pixels in brighter region to output pixels in full
region. That is what histogram equalization does.

Now we find the minimum histogram value (excluding 0) and apply the histogram equalization equation
as given in wiki page. But I have used here, the masked array concept array from Numpy. For masked
array, all operations are performed on non-masked elements. You can read more about it from Numpy
docs on masked arrays.
@code{.py}
cdf_m = np.ma.masked_equal(cdf,0)
cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())
cdf = np.ma.filled(cdf_m,0).astype('uint8')
@endcode
Now we have the look-up table that gives us the information on what is the output pixel value for
every input pixel value. So we just apply the transform.
@code{.py}
img2 = cdf[img]
@endcode
Now we calculate its histogram and cdf as before ( you do it) and result looks like below :

![image](images/histeq_numpy2.jpg)

Another important feature is that, even if the image was a darker image (instead of a brighter one
we used), after equalization we will get almost the same image as we got. As a result, this is used
as a "reference tool" to make all images with same lighting conditions. This is useful in many
cases. For example, in face recognition, before training the face data, the images of faces are
histogram equalized to make them all with same lighting conditions.

Histograms Equalization in OpenCV
---------------------------------

OpenCV has a function to do this, **cv.equalizeHist()**. Its input is just grayscale image and
output is our histogram equalized image.

Below is a simple code snippet showing its usage for same image we used :
@code{.py}
img = cv.imread('wiki.jpg', cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"
equ = cv.equalizeHist(img)
res = np.hstack((img,equ)) #stacking images side-by-side
cv.imwrite('res.png',res)
@endcode
![image](images/equalization_opencv.jpg)

So now you can take different images with different light conditions, equalize it and check the
results.

Histogram equalization is good when histogram of the image is confined to a particular region. It
won't work good in places where there is large intensity variations where histogram covers a large
region, ie both bright and dark pixels are present. Please check the SOF links in Additional
Resources.

CLAHE (Contrast Limited Adaptive Histogram Equalization)
--------------------------------------------------------

The first histogram equalization we just saw, considers the global contrast of the image. In many
cases, it is not a good idea. For example, below image shows an input image and its result after
global histogram equalization.

![image](images/clahe_1.jpg)

It is true that the background contrast has improved after histogram equalization. But compare the
face of statue in both images. We lost most of the information there due to over-brightness. It is
because its histogram is not confined to a particular region as we saw in previous cases (Try to
plot histogram of input image, you will get more intuition).

So to solve this problem, **adaptive histogram equalization** is used. In this, image is divided
into small blocks called "tiles" (tileSize is 8x8 by default in OpenCV). Then each of these blocks
are histogram equalized as usual. So in a small area, histogram would confine to a small region
(unless there is noise). If noise is there, it will be amplified. To avoid this, **contrast
limiting** is applied. If any histogram bin is above the specified contrast limit (by default 40 in
OpenCV), those pixels are clipped and distributed uniformly to other bins before applying histogram
equalization. After equalization, to remove artifacts in tile borders, bilinear interpolation is
applied.

Below code snippet shows how to apply CLAHE in OpenCV:
@code{.py}
import numpy as np
import cv2 as cv

img = cv.imread('tsukuba_l.png', cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"

# create a CLAHE object (Arguments are optional).
clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
cl1 = clahe.apply(img)

cv.imwrite('clahe_2.jpg',cl1)
@endcode
See the result below and compare it with results above, especially the statue region:

![image](images/clahe_2.jpg)

Additional Resources
--------------------

-#  Wikipedia page on [Histogram Equalization](http://en.wikipedia.org/wiki/Histogram_equalization)
2.  [Masked Arrays in Numpy](http://docs.scipy.org/doc/numpy/reference/maskedarray.html)

Also check these SOF questions regarding contrast adjustment:

-#  [How can I adjust contrast in OpenCV in
    C?](http://stackoverflow.com/questions/10549245/how-can-i-adjust-contrast-in-opencv-in-c)
4.  [How do I equalize contrast & brightness of images using
    opencv?](http://stackoverflow.com/questions/10561222/how-do-i-equalize-contrast-brightness-of-images-using-opencv)
