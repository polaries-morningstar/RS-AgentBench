# OpenCV Core: Getting Started with Images

Source: https://raw.githubusercontent.com/opencv/opencv/4.x/doc/tutorials/introduction/display_image/display_image.markdown

Getting Started with Images {#tutorial_display_image}
===========================

@prev_tutorial{tutorial_building_tegra_cuda}
@next_tutorial{tutorial_documentation}

|    |    |
| -: | :- |
| Original author | Ana Huamán |
| Compatibility | OpenCV >= 3.4.4 |

@tableofcontents

@warning
This tutorial can contain obsolete information.

Goal
----

In this tutorial you will learn how to:

-   Read an image from file (using @ref cv::imread)
-   Display an image in an OpenCV window (using @ref cv::imshow)
-   Write an image to a file (using @ref cv::imwrite)

Source Code
-----------

@add_toggle_cpp
-   **Downloadable code**: Click
    [here](https://github.com/opencv/opencv/tree/4.x/samples/cpp/tutorial_code/introduction/display_image/display_image.cpp)

-   **Code at glance:**
    @include samples/cpp/tutorial_code/introduction/display_image/display_image.cpp
@end_toggle

@add_toggle_python
-   **Downloadable code**: Click
    [here](https://github.com/opencv/opencv/tree/4.x/samples/python/tutorial_code/introduction/display_image/display_image.py)

-   **Code at glance:**
    @include samples/python/tutorial_code/introduction/display_image/display_image.py
@end_toggle


Explanation
-----------

@add_toggle_cpp
In OpenCV 3 we have multiple modules. Each one takes care of a different area or approach towards
image processing. You could already observe this in the structure of the user guide of these
tutorials itself. Before you use any of them you first need to include the header files where the
content of each individual module is declared.

You'll almost always end up using the:

- @ref core "core" section, as here are defined the basic building blocks of the library
- @ref imgcodecs "imgcodecs" module, which provides functions for reading and writing
- @ref highgui "highgui" module, as this contains the functions to show an image in a window

We also include the *iostream* to facilitate console line output and input.

By declaring `using namespace cv;`, in the following, the library functions can be accessed without explicitly stating the namespace.

@snippet cpp/tutorial_code/introduction/display_image/display_image.cpp includes
@end_toggle

@add_toggle_python
As a first step, the OpenCV python library is imported.
The proper way to do this is to additionally assign it the name *cv*, which is used in the following to reference the library.

@snippet samples/python/tutorial_code/introduction/display_image/display_image.py imports
@end_toggle

Now, let's analyze the main code.
As a first step, we read the image "starry_night.jpg" from the OpenCV samples.
In order to do so, a call to the @ref cv::imread function loads the image using the file path specified by the first argument.
The second argument is optional and specifies the format in which we want the image. This may be:

-   IMREAD_COLOR loads the image in the BGR 8-bit format. This is the **default** that is used here.
-   IMREAD_UNCHANGED loads the image as is (including the alpha channel if present)
-   IMREAD_GRAYSCALE loads the image as an intensity one

After reading in the image data will be stored in a @ref cv::Mat object.

@add_toggle_cpp
@snippet cpp/tutorial_code/introduction/display_image/display_image.cpp imread
@end_toggle

@add_toggle_python
@snippet samples/python/tutorial_code/introduction/display_image/display_image.py imread
@end_toggle

@note
   OpenCV offers support for the image formats Windows bitmap (bmp), portable image formats (pbm,
    pgm, ppm) and Sun raster (sr, ras). With help of plugins (you need to specify to use them if you
    build yourself the library, nevertheless in the packages we ship present by default) you may
    also load image formats like JPEG (jpeg, jpg, jpe), JPEG 2000 (jp2 - codenamed in the CMake as
    Jasper), TIFF files (tiff, tif) and portable network graphics (png). Furthermore, OpenEXR is
    also a possibility.

Afterwards, a check is executed, if the image was loaded correctly.
@add_toggle_cpp
@snippet cpp/tutorial_code/introduction/display_image/display_image.cpp empty
@end_toggle

@add_toggle_python
@snippet samples/python/tutorial_code/introduction/display_image/display_image.py empty
@end_toggle

Then, the image is shown using a call to the @ref cv::imshow function.
The first argument is the title of the window and the second argument is the @ref cv::Mat object that will be shown.

Because we want our window to be displayed until the user presses a key (otherwise the program would
end far too quickly), we use the @ref cv::waitKey function whose only parameter is just how long
should it wait for a user input (measured in milliseconds). Zero means to wait forever.
The return value is the key that was pressed.

@add_toggle_cpp
@snippet cpp/tutorial_code/introduction/display_image/display_image.cpp imshow
@end_toggle

@add_toggle_python
@snippet samples/python/tutorial_code/introduction/display_image/display_image.py imshow
@end_toggle

In the end, the image is written to a file if the pressed key was the "s"-key.
For this the cv::imwrite function is called that has the file path and the cv::Mat object as an argument.

@add_toggle_cpp
@snippet cpp/tutorial_code/introduction/display_image/display_image.cpp imsave
@end_toggle

@add_toggle_python
@snippet samples/python/tutorial_code/introduction/display_image/display_image.py imsave
@end_toggle

---
Source: https://raw.githubusercontent.com/opencv/opencv/4.x/doc/py_tutorials/py_core/py_basic_ops/py_basic_ops.markdown

Basic Operations on Images {#tutorial_py_basic_ops}
==========================

Goal
----

Learn to:

-   Access pixel values and modify them
-   Access image properties
-   Set a Region of Interest (ROI)
-   Split and merge images

Almost all the operations in this section are mainly related to Numpy rather than OpenCV. A good
knowledge of Numpy is required to write better optimized code with OpenCV.

*( Examples will be shown in a Python terminal, since most of them are just single lines of code )*

Accessing and Modifying pixel values
------------------------------------

Let's load a color image first:
@code{.py}
>>> import numpy as np
>>> import cv2 as cv

>>> img = cv.imread('messi5.jpg')
>>> assert img is not None, "file could not be read, check with os.path.exists()"
@endcode
You can access a pixel value by its row and column coordinates. For BGR image, it returns an array
of Blue, Green, Red values. For grayscale image, just corresponding intensity is returned.
@code{.py}
>>> px = img[100,100]
>>> print( px )
[157 166 200]

# accessing only blue pixel
>>> blue = img[100,100,0]
>>> print( blue )
157
@endcode
You can modify the pixel values the same way.
@code{.py}
>>> img[100,100] = [255,255,255]
>>> print( img[100,100] )
[255 255 255]
@endcode

**Warning**

Numpy is an optimized library for fast array calculations. So simply accessing each and every pixel
value and modifying it will be very slow and it is discouraged.

Accessing Image Properties
--------------------------

Image properties include number of rows, columns, and channels; type of image data; number of pixels; etc.

The shape of an image is accessed by img.shape. It returns a tuple of the number of rows, columns, and channels
(if the image is color):
@code{.py}
>>> print( img.shape )
(342, 548, 3)
@endcode

@note If an image is grayscale, the tuple returned contains only the number of rows
and columns, so it is a good method to check whether the loaded image is grayscale or color.

Total number of pixels is accessed by `img.size`:
@code{.py}
>>> print( img.size )
562248
@endcode
Image datatype is obtained by \`img.dtype\`:
@code{.py}
>>> print( img.dtype )
uint8
@endcode

@note img.dtype is very important while debugging because a large number of errors in OpenCV-Python
code are caused by invalid datatype.

Image ROI
---------

Sometimes, you will have to play with certain regions of images. For eye detection in images, first
face detection is done over the entire image. When a face is obtained, we select the face region alone
and search for eyes inside it instead of searching the whole image. It improves accuracy (because eyes
are always on faces :D ) and performance (because we search in a small area).

ROI is again obtained using Numpy indexing. Here I am selecting the ball and copying it to another
region in the image:
@code{.py}
>>> ball = img[280:340, 330:390]
>>> img[273:333, 100:160] = ball
@endcode
Check the results below:

![image](images/roi.jpg)

Splitting and Merging Image Channels
------------------------------------

Sometimes you will need to work separately on the B,G,R channels of an image. In this case, you need
to split the BGR image into single channels. In other cases, you may need to join these individual
channels to create a BGR image. You can do this simply by:
@code{.py}
>>> b,g,r = cv.split(img)
>>> img = cv.merge((b,g,r))
@endcode
Or
@code
>>> b = img[:,:,0]
@endcode
Suppose you want to set all the red pixels to zero - you do not need to split the channels first.
Numpy indexing is faster:
@code{.py}
>>> img[:,:,2] = 0
@endcode

**Warning**

cv.split() is a costly operation (in terms of time). So use it only if necessary. Otherwise go
for Numpy indexing.

Making Borders for Images (Padding)
-----------------------------------

If you want to create a border around an image, something like a photo frame, you can use
**cv.copyMakeBorder()**. But it has more applications for convolution operation, zero
padding etc. This function takes following arguments:

-   **src** - input image
-   **top**, **bottom**, **left**, **right** - border width in number of pixels in corresponding
    directions

-   **borderType** - Flag defining what kind of border to be added. It can be following types:
    -   **cv.BORDER_CONSTANT** - Adds a constant colored border. The value should be given
        as next argument.
    -   **cv.BORDER_REFLECT** - Border will be mirror reflection of the border elements,
        like this : *fedcba|abcdefgh|hgfedcb*
    -   **cv.BORDER_REFLECT_101** or **cv.BORDER_DEFAULT** - Same as above, but with a
        slight change, like this : *gfedcb|abcdefgh|gfedcba*
    -   **cv.BORDER_REPLICATE** - Last element is replicated throughout, like this:
        *aaaaaa|abcdefgh|hhhhhhh*
    -   **cv.BORDER_WRAP** - Can't explain, it will look like this :
        *cdefgh|abcdefgh|abcdefg*

-   **value** - Color of border if border type is cv.BORDER_CONSTANT

Below is a sample code demonstrating all these border types for better understanding:
@code{.py}
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

BLUE = [255,0,0]

img1 = cv.imread('opencv-logo.png')
assert img1 is not None, "file could not be read, check with os.path.exists()"

replicate = cv.copyMakeBorder(img1,10,10,10,10,cv.BORDER_REPLICATE)
reflect = cv.copyMakeBorder(img1,10,10,10,10,cv.BORDER_REFLECT)
reflect101 = cv.copyMakeBorder(img1,10,10,10,10,cv.BORDER_REFLECT_101)
wrap = cv.copyMakeBorder(img1,10,10,10,10,cv.BORDER_WRAP)
constant= cv.copyMakeBorder(img1,10,10,10,10,cv.BORDER_CONSTANT,value=BLUE)

plt.subplot(231),plt.imshow(img1,'gray'),plt.title('ORIGINAL')
plt.subplot(232),plt.imshow(replicate,'gray'),plt.title('REPLICATE')
plt.subplot(233),plt.imshow(reflect,'gray'),plt.title('REFLECT')
plt.subplot(234),plt.imshow(reflect101,'gray'),plt.title('REFLECT_101')
plt.subplot(235),plt.imshow(wrap,'gray'),plt.title('WRAP')
plt.subplot(236),plt.imshow(constant,'gray'),plt.title('CONSTANT')

plt.show()
@endcode
See the result below. (Image is displayed with matplotlib. So RED and BLUE channels will be
interchanged):

![image](images/border.jpg)

---
Source: https://raw.githubusercontent.com/opencv/opencv/4.x/doc/py_tutorials/py_core/py_image_arithmetics/py_image_arithmetics.markdown

Arithmetic Operations on Images {#tutorial_py_image_arithmetics}
===============================

Goal
----

-   Learn several arithmetic operations on images, like addition, subtraction, bitwise operations, and etc.
-   Learn these functions: **cv.add()**, **cv.addWeighted()**, etc.

Image Addition
--------------

You can add two images with the OpenCV function, cv.add(), or simply by the numpy operation
res = img1 + img2. Both images should be of same depth and type, or the second image can just be a
scalar value.

@note There is a difference between OpenCV addition and Numpy addition. OpenCV addition is a
saturated operation while Numpy addition is a modulo operation.

For example, consider the below sample:
@code{.py}
>>> x = np.uint8([250])
>>> y = np.uint8([10])

>>> print( cv.add(x,y) ) # 250+10 = 260 => 255
[[255]]

>>> print( x+y )          # 250+10 = 260 % 256 = 4
[4]
@endcode
This will be more visible when you add two images. Stick with OpenCV functions, because they will provide a better result.

Image Blending
--------------

This is also image addition, but different weights are given to images in order to give a feeling of
blending or transparency. Images are added as per the equation below:

\f[g(x) = (1 - \alpha)f_{0}(x) + \alpha f_{1}(x)\f]

By varying \f$\alpha\f$ from \f$0 \rightarrow 1\f$, you can perform a cool transition between one image to
another.

Here I took two images to blend together. The first image is given a weight of 0.7 and the second image
is given 0.3. cv.addWeighted() applies the following equation to the image:

\f[dst = \alpha \cdot img1 + \beta \cdot img2 + \gamma\f]

Here \f$\gamma\f$ is taken as zero.
@code{.py}
img1 = cv.imread('ml.png')
img2 = cv.imread('opencv-logo.png')
assert img1 is not None, "file could not be read, check with os.path.exists()"
assert img2 is not None, "file could not be read, check with os.path.exists()"

dst = cv.addWeighted(img1,0.7,img2,0.3,0)

cv.imshow('dst',dst)
cv.waitKey(0)
cv.destroyAllWindows()
@endcode
Check the result below:

![image](images/blending.jpg)

Bitwise Operations
------------------

This includes the bitwise AND, OR, NOT, and XOR operations. They will be highly useful while extracting
any part of the image (as we will see in coming chapters), defining and working with non-rectangular
ROI's, and etc. Below we will see an example of how to change a particular region of an image.

I want to put the OpenCV logo above an image. If I add two images, it will change the color. If I blend them,
I get a transparent effect. But I want it to be opaque. If it was a rectangular region, I could use
ROI as we did in the last chapter. But the OpenCV logo is a not a rectangular shape. So you can do it with
bitwise operations as shown below:
@code{.py}
# Load two images
img1 = cv.imread('messi5.jpg')
img2 = cv.imread('opencv-logo-white.png')
assert img1 is not None, "file could not be read, check with os.path.exists()"
assert img2 is not None, "file could not be read, check with os.path.exists()"

# I want to put logo on top-left corner, So I create a ROI
rows,cols,channels = img2.shape
roi = img1[0:rows, 0:cols]

# Now create a mask of logo and create its inverse mask also
img2gray = cv.cvtColor(img2,cv.COLOR_BGR2GRAY)
ret, mask = cv.threshold(img2gray, 10, 255, cv.THRESH_BINARY)
mask_inv = cv.bitwise_not(mask)

# Now black-out the area of logo in ROI
img1_bg = cv.bitwise_and(roi,roi,mask = mask_inv)

# Take only region of logo from logo image.
img2_fg = cv.bitwise_and(img2,img2,mask = mask)

# Put logo in ROI and modify the main image
dst = cv.add(img1_bg,img2_fg)
img1[0:rows, 0:cols ] = dst

cv.imshow('res',img1)
cv.waitKey(0)
cv.destroyAllWindows()
@endcode
See the result below. Left image shows the mask we created. Right image shows the final result. For
more understanding, display all the intermediate images in the above code, especially img1_bg and
img2_fg.

![image](images/overlay.jpg)

Exercises
---------

-#  Create a slide show of images in a folder with smooth transition between images using
    cv.addWeighted function

---
Source: https://raw.githubusercontent.com/opencv/opencv/4.x/doc/py_tutorials/py_imgproc/py_colorspaces/py_colorspaces.markdown

Changing Colorspaces {#tutorial_py_colorspaces}
====================

Goal
----

-   In this tutorial, you will learn how to convert images from one color-space to another, like
    BGR \f$\leftrightarrow\f$ Gray, BGR \f$\leftrightarrow\f$ HSV, etc.
-   In addition to that, we will create an application to extract a colored object in a video
-   You will learn the following functions: **cv.cvtColor()**, **cv.inRange()**, etc.

Changing Color-space
--------------------

There are more than 150 color-space conversion methods available in OpenCV. But we will look into
only two, which are most widely used ones: BGR \f$\leftrightarrow\f$ Gray and BGR \f$\leftrightarrow\f$ HSV.

For color conversion, we use the function cv.cvtColor(input_image, flag) where flag determines the
type of conversion.

For BGR \f$\rightarrow\f$ Gray conversion, we use the flag cv.COLOR_BGR2GRAY. Similarly for BGR
\f$\rightarrow\f$ HSV, we use the flag cv.COLOR_BGR2HSV. To get other flags, just run following
commands in your Python terminal:
@code{.py}
>>> import cv2 as cv
>>> flags = [i for i in dir(cv) if i.startswith('COLOR_')]
>>> print( flags )
@endcode
@note For HSV, hue range is [0,179], saturation range is [0,255], and value range is [0,255].
Different software use different scales. So if you are comparing OpenCV values with them, you need
to normalize these ranges.

Object Tracking
---------------

Now that we know how to convert a BGR image to HSV, we can use this to extract a colored object. In HSV, it
is easier to represent a color than in BGR color-space. In our application, we will try to extract
a blue colored object. So here is the method:

-   Take each frame of the video
-   Convert from BGR to HSV color-space
-   We threshold the HSV image for a range of blue color
-   Now extract the blue object alone, we can do whatever we want on that image.

Below is the code which is commented in detail:
@code{.py}
import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)

while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])

    # Threshold the HSV image to get only blue colors
    mask = cv.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv.bitwise_and(frame,frame, mask= mask)

    cv.imshow('frame',frame)
    cv.imshow('mask',mask)
    cv.imshow('res',res)
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

cv.destroyAllWindows()
@endcode
Below image shows tracking of the blue object:

![image](images/frame.jpg)

@note There is some noise in the image. We will see how to remove it in later chapters.

@note This is the simplest method in object tracking. Once you learn functions of contours, you can
do plenty of things like find the centroid of an object and use it to track the object, draw diagrams
just by moving your hand in front of a camera, and other fun stuff.

How to find HSV values to track?
--------------------------------

This is a common question found in [stackoverflow.com](http://www.stackoverflow.com). It is very simple and
you can use the same function, cv.cvtColor(). Instead of passing an image, you just pass the BGR
values you want. For example, to find the HSV value of Green, try the following commands in a Python
terminal:
@code{.py}
>>> green = np.uint8([[[0,255,0 ]]])
>>> hsv_green = cv.cvtColor(green,cv.COLOR_BGR2HSV)
>>> print( hsv_green )
[[[ 60 255 255]]]
@endcode
Now you take [H-10, 100,100] and [H+10, 255, 255] as the lower bound and upper bound respectively. Apart
from this method, you can use any image editing tools like GIMP or any online converters to find
these values, but don't forget to adjust the HSV ranges.

Exercises
---------

-#  Try to find a way to extract more than one colored object, for example, extract red, blue, and green
objects simultaneously.
