# OpenCV Contours: Getting Started & Contour Properties

Source: https://raw.githubusercontent.com/opencv/opencv/4.x/doc/py_tutorials/py_imgproc/py_contours/py_contours_begin/py_contours_begin.markdown
Source: https://raw.githubusercontent.com/opencv/opencv/4.x/doc/py_tutorials/py_imgproc/py_contours/py_contour_properties/py_contour_properties.markdown

---

## Part 1: Contours -- Getting Started

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
```python
import numpy as np
import cv2 as cv

im = cv.imread('test.jpg')
assert im is not None, "file could not be read, check with os.path.exists()"
imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(imgray, 127, 255, 0)
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
```
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
```python
cv.drawContours(img, contours, -1, (0,255,0), 3)
```
* To draw an individual contour, say 4th contour:
```python
cv.drawContours(img, contours, 3, (0,255,0), 3)
```
* But most of the time, below method will be useful:
```python
cnt = contours[4]
cv.drawContours(img, [cnt], 0, (0,255,0), 3)
```

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

---

## Part 2: Contour Properties

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

Aspect Ratio = Width / Height

```python
x,y,w,h = cv.boundingRect(cnt)
aspect_ratio = float(w)/h
```

2. Extent
---------

Extent is the ratio of contour area to bounding rectangle area.

Extent = Object Area / Bounding Rectangle Area

```python
area = cv.contourArea(cnt)
x,y,w,h = cv.boundingRect(cnt)
rect_area = w*h
extent = float(area)/rect_area
```

3. Solidity
-----------

Solidity is the ratio of contour area to its convex hull area.

Solidity = Contour Area / Convex Hull Area

```python
area = cv.contourArea(cnt)
hull = cv.convexHull(cnt)
hull_area = cv.contourArea(hull)
solidity = float(area)/hull_area
```

4. Equivalent Diameter
----------------------

Equivalent Diameter is the diameter of the circle whose area is same as the contour area.

Equivalent Diameter = sqrt(4 * Contour Area / pi)

```python
area = cv.contourArea(cnt)
equi_diameter = np.sqrt(4*area/np.pi)
```

5. Orientation
--------------

Orientation is the angle at which object is directed. Following method also gives the Major Axis and
Minor Axis lengths.
```python
(x,y),(MA,ma),angle = cv.fitEllipse(cnt)
```

6. Mask and Pixel Points
------------------------

In some cases, we may need all the points which comprises that object. It can be done as follows:
```python
mask = np.zeros(imgray.shape,np.uint8)
cv.drawContours(mask,[cnt],0,255,-1)
pixelpoints = np.transpose(np.nonzero(mask))
#pixelpoints = cv.findNonZero(mask)
```
Here, two methods, one using Numpy functions, next one using OpenCV function (last commented line)
are given to do the same. Results are also same, but with a slight difference. Numpy gives
coordinates in **(row, column)** format, while OpenCV gives coordinates in **(x,y)** format. So
basically the answers will be interchanged. Note that, **row = y** and **column = x**.

7. Maximum Value, Minimum Value and their locations
---------------------------------------------------

We can find these parameters using a mask image.
```python
min_val, max_val, min_loc, max_loc = cv.minMaxLoc(imgray,mask = mask)
```

8. Mean Color or Mean Intensity
-------------------------------

Here, we can find the average color of an object. Or it can be average intensity of the object in
grayscale mode. We again use the same mask to do it.
```python
mean_val = cv.mean(im,mask = mask)
```

9. Extreme Points
-----------------

Extreme Points means topmost, bottommost, rightmost and leftmost points of the object.
```python
leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])
```

Exercises
---------

-#  There are still some features left in matlab regionprops doc. Try to implement them.
