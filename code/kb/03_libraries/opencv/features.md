# OpenCV Features: Harris Corner Detection

Source: https://raw.githubusercontent.com/opencv/opencv/4.x/doc/py_tutorials/py_feature2d/py_features_harris/py_features_harris.markdown

Harris Corner Detection {#tutorial_py_features_harris}
=======================

Goal
----

In this chapter,

-   We will understand the concepts behind Harris Corner Detection.
-   We will see the following functions: **cv.cornerHarris()**, **cv.cornerSubPix()**

Theory
------

In the last chapter, we saw that corners are regions in the image with large variation in intensity in
all the directions. One early attempt to find these corners was done by **Chris Harris & Mike
Stephens** in their paper **A Combined Corner and Edge Detector** in 1988, so now it is called
the Harris Corner Detector. He took this simple idea to a mathematical form. It basically finds the
difference in intensity for a displacement of \f$(u,v)\f$ in all directions. This is expressed as below:

\f[E(u,v) = \sum_{x,y} \underbrace{w(x,y)}_\text{window function} \, [\underbrace{I(x+u,y+v)}_\text{shifted intensity}-\underbrace{I(x,y)}_\text{intensity}]^2\f]

The window function is either a rectangular window or a Gaussian window which gives weights to pixels
underneath.

We have to maximize this function \f$E(u,v)\f$ for corner detection. That means we have to maximize the
second term. Applying Taylor Expansion to the above equation and using some mathematical steps (please
refer to any standard text books you like for full derivation), we get the final equation as:

\f[E(u,v) \approx \begin{bmatrix} u & v \end{bmatrix} M \begin{bmatrix} u \\ v \end{bmatrix}\f]

where

\f[M = \sum_{x,y} w(x,y) \begin{bmatrix}I_x I_x & I_x I_y \\
                                     I_x I_y & I_y I_y \end{bmatrix}\f]

Here, \f$I_x\f$ and \f$I_y\f$ are image derivatives in x and y directions respectively. (These can be easily found
using **cv.Sobel()**).

Then comes the main part. After this, they created a score, basically an equation, which
determines if a window can contain a corner or not.

\f[R = \det(M) - k(\operatorname{trace}(M))^2\f]

where
    -   \f$\det(M) = \lambda_1 \lambda_2\f$
    -   \f$\operatorname{trace}(M) = \lambda_1 + \lambda_2\f$
    -   \f$\lambda_1\f$ and \f$\lambda_2\f$ are the eigenvalues of \f$M\f$

So the magnitudes of these eigenvalues decide whether a region is a corner, an edge, or flat.

-   When \f$|R|\f$ is small, which happens when \f$\lambda_1\f$ and \f$\lambda_2\f$ are small, the region is
    flat.
-   When \f$R<0\f$, which happens when \f$\lambda_1 >> \lambda_2\f$ or vice versa, the region is edge.
-   When \f$R\f$ is large, which happens when \f$\lambda_1\f$ and \f$\lambda_2\f$ are large and
    \f$\lambda_1 \sim \lambda_2\f$, the region is a corner.

It can be represented in a nice picture as follows:

![image](images/harris_region.jpg)

So the result of Harris Corner Detection is a grayscale image with these scores. Thresholding for a
suitable score gives you the corners in the image. We will do it with a simple image.

Harris Corner Detector in OpenCV
--------------------------------

OpenCV has the function **cv.cornerHarris()** for this purpose. Its arguments are:

-   **img** - Input image. It should be grayscale and float32 type.
-   **blockSize** - It is the size of neighbourhood considered for corner detection
-   **ksize** - Aperture parameter of the Sobel derivative used.
-   **k** - Harris detector free parameter in the equation.

See the example below:
@code{.py}
import numpy as np
import cv2 as cv

filename = 'chessboard.png'
img = cv.imread(filename)
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

gray = np.float32(gray)
dst = cv.cornerHarris(gray,2,3,0.04)

#result is dilated for marking the corners, not important
dst = cv.dilate(dst,None)

# Threshold for an optimal value, it may vary depending on the image.
img[dst>0.01*dst.max()]=[0,0,255]

cv.imshow('dst',img)
if cv.waitKey(0) & 0xff == 27:
    cv.destroyAllWindows()
@endcode
Below are the three results:

![image](images/harris_result.jpg)

Corner with SubPixel Accuracy
-----------------------------

Sometimes, you may need to find the corners with maximum accuracy. OpenCV comes with a function
**cv.cornerSubPix()** which further refines the corners detected with sub-pixel accuracy. Below is
an example. As usual, we need to find the Harris corners first. Then we pass the centroids of these
corners (There may be a bunch of pixels at a corner, we take their centroid) to refine them. Harris
corners are marked in red pixels and refined corners are marked in green pixels. For this function,
we have to define the criteria when to stop the iteration. We stop it after a specified number of
iterations or a certain accuracy is achieved, whichever occurs first. We also need to define the size
of the neighbourhood it searches for corners.
@code{.py}
import numpy as np
import cv2 as cv

filename = 'chessboard2.jpg'
img = cv.imread(filename)
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

# find Harris corners
gray = np.float32(gray)
dst = cv.cornerHarris(gray,2,3,0.04)
dst = cv.dilate(dst,None)
ret, dst = cv.threshold(dst,0.01*dst.max(),255,0)
dst = np.uint8(dst)

# find centroids
ret, labels, stats, centroids = cv.connectedComponentsWithStats(dst)

# define the criteria to stop and refine the corners
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.001)
corners = cv.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)

# Now draw them
res = np.hstack((centroids,corners))
res = np.int0(res)
img[res[:,1],res[:,0]]=[0,0,255]
img[res[:,3],res[:,2]] = [0,255,0]

cv.imwrite('subpixel5.png',img)
@endcode
Below is the result, where some important locations are shown in the zoomed window to visualize:

![image](images/subpixel3.png)

Additional Resources
--------------------

Exercises
---------

---
Source: https://raw.githubusercontent.com/opencv/opencv/4.x/doc/py_tutorials/py_feature2d/py_sift_intro/py_sift_intro.markdown

Introduction to SIFT (Scale-Invariant Feature Transform) {#tutorial_py_sift_intro}
========================================================

Goal
----

In this chapter,
    -   We will learn about the concepts of SIFT algorithm
    -   We will learn to find SIFT Keypoints and Descriptors.

Theory
------

In last couple of chapters, we saw some corner detectors like Harris etc. They are
rotation-invariant, which means, even if the image is rotated, we can find the same corners. It is
obvious because corners remain corners in rotated image also. But what about scaling? A corner may
not be a corner if the image is scaled. For example, check a simple image below. A corner in a small
image within a small window is flat when it is zoomed in the same window. So Harris corner is not
scale invariant.

![image](images/sift_scale_invariant.jpg)

In 2004, **D.Lowe**, University of British Columbia, came up with a new algorithm, Scale
Invariant Feature Transform (SIFT) in his paper, **Distinctive Image Features from Scale-Invariant
Keypoints**, which extract keypoints and compute its descriptors. *(This paper is easy to understand
and considered to be best material available on SIFT. This explanation is just a short summary of
this paper)*.

There are mainly four steps involved in SIFT algorithm. We will see them one-by-one.

### 1. Scale-space Extrema Detection

From the image above, it is obvious that we can't use the same window to detect keypoints with
different scale. It is OK with small corner. But to detect larger corners we need larger windows.
For this, scale-space filtering is used. In it, Laplacian of Gaussian is found for the image with
various \f$\sigma\f$ values. LoG acts as a blob detector which detects blobs in various sizes due to
change in \f$\sigma\f$. In short, \f$\sigma\f$ acts as a scaling parameter. For eg, in the above image,
gaussian kernel with low \f$\sigma\f$ gives high value for small corner while gaussian kernel with high
\f$\sigma\f$ fits well for larger corner. So, we can find the local maxima across the scale and space
which gives us a list of \f$(x,y,\sigma)\f$ values which means there is a potential keypoint at (x,y) at
\f$\sigma\f$ scale.

But this LoG is a little costly, so SIFT algorithm uses Difference of Gaussians which is an
approximation of LoG. Difference of Gaussian is obtained as the difference of Gaussian blurring of
an image with two different \f$\sigma\f$, let it be \f$\sigma\f$ and \f$k\sigma\f$. This process is done for
different octaves of the image in Gaussian Pyramid. It is represented in below image:

![image](images/sift_dog.jpg)

Once this DoG are found, images are searched for local extrema over scale and space. For eg, one
pixel in an image is compared with its 8 neighbours as well as 9 pixels in next scale and 9 pixels
in previous scales. If it is a local extrema, it is a potential keypoint. It basically means that
keypoint is best represented in that scale. It is shown in below image:

![image](images/sift_local_extrema.jpg)

Regarding different parameters, the paper gives some empirical data which can be summarized as,
number of octaves = 4, number of scale levels = 5, initial \f$\sigma=1.6\f$, \f$k=\sqrt{2}\f$ etc as optimal
values.

### 2. Keypoint Localization

Once potential keypoints locations are found, they have to be refined to get more accurate results.
They used Taylor series expansion of scale space to get more accurate location of extrema, and if
the intensity at this extrema is less than a threshold value (0.03 as per the paper), it is
rejected. This threshold is called **contrastThreshold** in OpenCV

DoG has higher response for edges, so edges also need to be removed. For this, a concept similar to
Harris corner detector is used. They used a 2x2 Hessian matrix (H) to compute the principal
curvature. We know from Harris corner detector that for edges, one eigen value is larger than the
other. So here they used a simple function,

If this ratio is greater than a threshold, called **edgeThreshold** in OpenCV, that keypoint is
discarded. It is given as 10 in paper.

So it eliminates any low-contrast keypoints and edge keypoints and what remains is strong interest
points.

### 3. Orientation Assignment

Now an orientation is assigned to each keypoint to achieve invariance to image rotation. A
neighbourhood is taken around the keypoint location depending on the scale, and the gradient
magnitude and direction is calculated in that region. An orientation histogram with 36 bins covering
360 degrees is created (It is weighted by gradient magnitude and gaussian-weighted circular window
with \f$\sigma\f$ equal to 1.5 times the scale of keypoint). The highest peak in the histogram is taken
and any peak above 80% of it is also considered to calculate the orientation. It creates keypoints
with same location and scale, but different directions. It contribute to stability of matching.

### 4. Keypoint Descriptor

Now keypoint descriptor is created. A 16x16 neighbourhood around the keypoint is taken. It is
divided into 16 sub-blocks of 4x4 size. For each sub-block, 8 bin orientation histogram is created.
So a total of 128 bin values are available. It is represented as a vector to form keypoint
descriptor. In addition to this, several measures are taken to achieve robustness against
illumination changes, rotation etc.

### 5. Keypoint Matching

Keypoints between two images are matched by identifying their nearest neighbours. But in some cases,
the second closest-match may be very near to the first. It may happen due to noise or some other
reasons. In that case, ratio of closest-distance to second-closest distance is taken. If it is
greater than 0.8, they are rejected. It eliminates around 90% of false matches while discards only
5% correct matches, as per the paper.

This is a summary of SIFT algorithm. For more details and understanding, reading the original
paper is highly recommended.

SIFT in OpenCV
--------------

Now let's see SIFT functionalities available in OpenCV. Note that these were previously only
available in [the opencv contrib repo](https://github.com/opencv/opencv_contrib), but the patent
expired in the year 2020. So they are now included in the main repo. Let's start with keypoint
detection and draw them. First we have to construct a SIFT object. We can pass different
parameters to it which are optional and they are well explained in docs.
@code{.py}
import numpy as np
import cv2 as cv

img = cv.imread('home.jpg')
gray= cv.cvtColor(img,cv.COLOR_BGR2GRAY)

sift = cv.SIFT_create()
kp = sift.detect(gray,None)

img=cv.drawKeypoints(gray,kp,img)

cv.imwrite('sift_keypoints.jpg',img)
@endcode
**sift.detect()** function finds the keypoint in the images. You can pass a mask if you want to
search only a part of image. Each keypoint is a special structure which has many attributes like its
(x,y) coordinates, size of the meaningful neighbourhood, angle which specifies its orientation,
response that specifies strength of keypoints etc.

OpenCV also provides **cv.drawKeyPoints()** function which draws the small circles on the locations
of keypoints. If you pass a flag, **cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS** to it, it will
draw a circle with size of keypoint and it will even show its orientation. See below example.
@code{.py}
img=cv.drawKeypoints(gray,kp,img,flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv.imwrite('sift_keypoints.jpg',img)
@endcode
See the two results below:

![image](images/sift_keypoints.jpg)

Now to calculate the descriptor, OpenCV provides two methods.

-#  Since you already found keypoints, you can call **sift.compute()** which computes the
    descriptors from the keypoints we have found. Eg: kp,des = sift.compute(gray,kp)
2.  If you didn't find keypoints, directly find keypoints and descriptors in a single step with the
    function, **sift.detectAndCompute()**.

We will see the second method:
@code{.py}
sift = cv.SIFT_create()
kp, des = sift.detectAndCompute(gray,None)
@endcode
Here kp will be a list of keypoints and des is a numpy array of shape
\f$\text{(Number of Keypoints)} \times 128\f$.

So we got keypoints, descriptors etc. Now we want to see how to match keypoints in different images.
That we will learn in coming chapters.

---
Source: https://raw.githubusercontent.com/opencv/opencv/4.x/doc/py_tutorials/py_feature2d/py_orb/py_orb.markdown

ORB (Oriented FAST and Rotated BRIEF) {#tutorial_py_orb}
=====================================

Goal
----

In this chapter,
    -   We will see the basics of ORB

Theory
------

As an OpenCV enthusiast, the most important thing about the ORB is that it came from "OpenCV Labs".
This algorithm was brought up by Ethan Rublee, Vincent Rabaud, Kurt Konolige and Gary R. Bradski in
their paper **ORB: An efficient alternative to SIFT or SURF** in 2011. As the title says, it is a
good alternative to SIFT and SURF in computation cost, matching performance and mainly the patents.
Yes, SIFT and SURF are patented and you are supposed to pay them for its use. But ORB is not !!!

ORB is basically a fusion of FAST keypoint detector and BRIEF descriptor with many modifications to
enhance the performance. First it use FAST to find keypoints, then apply Harris corner measure to
find top N points among them. It also use pyramid to produce multiscale-features. But one problem is
that, FAST doesn't compute the orientation. So what about rotation invariance? Authors came up with
following modification.

It computes the intensity weighted centroid of the patch with located corner at center. The
direction of the vector from this corner point to centroid gives the orientation. To improve the
rotation invariance, moments are computed with x and y which should be in a circular region of
radius \f$r\f$, where \f$r\f$ is the size of the patch.

Now for descriptors, ORB use BRIEF descriptors. But we have already seen that BRIEF performs poorly
with rotation. So what ORB does is to "steer" BRIEF according to the orientation of keypoints. For
any feature set of \f$n\f$ binary tests at location \f$(x_i, y_i)\f$, define a \f$2 \times n\f$ matrix, \f$S\f$
which contains the coordinates of these pixels. Then using the orientation of patch, \f$\theta\f$, its
rotation matrix is found and rotates the \f$S\f$ to get steered(rotated) version \f$S_\theta\f$.

ORB discretize the angle to increments of \f$2 \pi /30\f$ (12 degrees), and construct a lookup table of
precomputed BRIEF patterns. As long as the keypoint orientation \f$\theta\f$ is consistent across views,
the correct set of points \f$S_\theta\f$ will be used to compute its descriptor.

BRIEF has an important property that each bit feature has a large variance and a mean near 0.5. But
once it is oriented along keypoint direction, it loses this property and become more distributed.
High variance makes a feature more discriminative, since it responds differentially to inputs.
Another desirable property is to have the tests uncorrelated, since then each test will contribute
to the result. To resolve all these, ORB runs a greedy search among all possible binary tests to
find the ones that have both high variance and means close to 0.5, as well as being uncorrelated.
The result is called **rBRIEF**.

For descriptor matching, multi-probe LSH which improves on the traditional LSH, is used. The paper
says ORB is much faster than SURF and SIFT and ORB descriptor works better than SURF. ORB is a good
choice in low-power devices for panorama stitching etc.

ORB in OpenCV
-------------

As usual, we have to create an ORB object with the function, **cv.ORB()** or using feature2d common
interface. It has a number of optional parameters. Most useful ones are nFeatures which denotes
maximum number of features to be retained (by default 500), scoreType which denotes whether Harris
score or FAST score to rank the features (by default, Harris score) etc. Another parameter, WTA_K
decides number of points that produce each element of the oriented BRIEF descriptor. By default it
is two, ie selects two points at a time. In that case, for matching, NORM_HAMMING distance is used.
If WTA_K is 3 or 4, which takes 3 or 4 points to produce BRIEF descriptor, then matching distance
is defined by NORM_HAMMING2.

Below is a simple code which shows the use of ORB.
@code{.py}
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

img = cv.imread('simple.jpg', cv.IMREAD_GRAYSCALE)

# Initiate ORB detector
orb = cv.ORB_create()

# find the keypoints with ORB
kp = orb.detect(img,None)

# compute the descriptors with ORB
kp, des = orb.compute(img, kp)

# draw only keypoints location,not size and orientation
img2 = cv.drawKeypoints(img, kp, None, color=(0,255,0), flags=0)
plt.imshow(img2), plt.show()
@endcode
See the result below:

![image](images/orb_kp.jpg)

ORB feature matching, we will do in another chapter.

Additional Resources
--------------------

-#  Ethan Rublee, Vincent Rabaud, Kurt Konolige, Gary R. Bradski: ORB: An efficient alternative to
    SIFT or SURF. ICCV 2011: 2564-2571.

---
Source: https://raw.githubusercontent.com/opencv/opencv/4.x/doc/py_tutorials/py_feature2d/py_matcher/py_matcher.markdown

Feature Matching {#tutorial_py_matcher}
================

Goal
----

In this chapter
    -   We will see how to match features in one image with others.
    -   We will use the Brute-Force matcher and FLANN Matcher in OpenCV

Basics of Brute-Force Matcher
-----------------------------

Brute-Force matcher is simple. It takes the descriptor of one feature in first set and is matched
with all other features in second set using some distance calculation. And the closest one is
returned.

For BF matcher, first we have to create the BFMatcher object using **cv.BFMatcher()**. It takes two
optional params. First one is normType. It specifies the distance measurement to be used. By
default, it is cv.NORM_L2. It is good for SIFT, SURF etc (cv.NORM_L1 is also there). For binary
string based descriptors like ORB, BRIEF, BRISK etc, cv.NORM_HAMMING should be used, which used
Hamming distance as measurement. If ORB is using WTA_K == 3 or 4, cv.NORM_HAMMING2 should be
used.

Second param is boolean variable, crossCheck which is false by default. If it is true, Matcher
returns only those matches with value (i,j) such that i-th descriptor in set A has j-th descriptor
in set B as the best match and vice-versa. That is, the two features in both sets should match each
other. It provides consistent result, and is a good alternative to ratio test proposed by D.Lowe in
SIFT paper.

Once it is created, two important methods are *BFMatcher.match()* and *BFMatcher.knnMatch()*. First
one returns the best match. Second method returns k best matches where k is specified by the user.
It may be useful when we need to do additional work on that.

Like we used cv.drawKeypoints() to draw keypoints, **cv.drawMatches()** helps us to draw the
matches. It stacks two images horizontally and draw lines from first image to second image showing
best matches. There is also **cv.drawMatchesKnn** which draws all the k best matches. If k=2, it
will draw two match-lines for each keypoint. So we have to pass a mask if we want to selectively
draw it.

Let's see one example for each of SIFT and ORB (Both use different distance measurements).

### Brute-Force Matching with ORB Descriptors

Here, we will see a simple example on how to match features between two images. In this case, I have
a queryImage and a trainImage. We will try to find the queryImage in trainImage using feature
matching. ( The images are /samples/data/box.png and /samples/data/box_in_scene.png)

We are using ORB descriptors to match features. So let's start with loading images, finding
descriptors etc.
@code{.py}
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

img1 = cv.imread('box.png',cv.IMREAD_GRAYSCALE)          # queryImage
img2 = cv.imread('box_in_scene.png',cv.IMREAD_GRAYSCALE) # trainImage

# Initiate ORB detector
orb = cv.ORB_create()

# find the keypoints and descriptors with ORB
kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)
@endcode
Next we create a BFMatcher object with distance measurement cv.NORM_HAMMING (since we are using
ORB) and crossCheck is switched on for better results. Then we use Matcher.match() method to get the
best matches in two images. We sort them in ascending order of their distances so that best matches
(with low distance) come to front. Then we draw only first 10 matches (Just for sake of visibility.
You can increase it as you like)
@code{.py}
# create BFMatcher object
bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)

# Match descriptors.
matches = bf.match(des1,des2)

# Sort them in the order of their distance.
matches = sorted(matches, key = lambda x:x.distance)

# Draw first 10 matches.
img3 = cv.drawMatches(img1,kp1,img2,kp2,matches[:10],None,flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

plt.imshow(img3),plt.show()
@endcode
Below is the result I got:

![image](images/matcher_result1.jpg)

### What is this Matcher Object?

The result of matches = bf.match(des1,des2) line is a list of DMatch objects. This DMatch object has
following attributes:

-   DMatch.distance - Distance between descriptors. The lower, the better it is.
-   DMatch.trainIdx - Index of the descriptor in train descriptors
-   DMatch.queryIdx - Index of the descriptor in query descriptors
-   DMatch.imgIdx - Index of the train image.

### Brute-Force Matching with SIFT Descriptors and Ratio Test

This time, we will use BFMatcher.knnMatch() to get k best matches. In this example, we will take k=2
so that we can apply ratio test explained by D.Lowe in his paper.
@code{.py}
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

img1 = cv.imread('box.png',cv.IMREAD_GRAYSCALE)          # queryImage
img2 = cv.imread('box_in_scene.png',cv.IMREAD_GRAYSCALE) # trainImage

# Initiate SIFT detector
sift = cv.SIFT_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

# BFMatcher with default params
bf = cv.BFMatcher()
matches = bf.knnMatch(des1,des2,k=2)

# Apply ratio test
good = []
for m,n in matches:
    if m.distance < 0.75*n.distance:
        good.append([m])

# cv.drawMatchesKnn expects list of lists as matches.
img3 = cv.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

plt.imshow(img3),plt.show()
@endcode
See the result below:

![image](images/matcher_result2.jpg)

FLANN based Matcher
-------------------

FLANN stands for Fast Library for Approximate Nearest Neighbors. It contains a collection of
algorithms optimized for fast nearest neighbor search in large datasets and for high dimensional
features. It works faster than BFMatcher for large datasets. We will see the second example
with FLANN based matcher.

For FLANN based matcher, we need to pass two dictionaries which specifies the algorithm to be used,
its related parameters etc. First one is IndexParams. For various algorithms, the information to be
passed is explained in FLANN docs. As a summary, for algorithms like SIFT, SURF etc. you can pass
following:
@code{.py}
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
@endcode
While using ORB, you can pass the following. The commented values are recommended as per the docs,
but it didn't provide required results in some cases. Other values worked fine.:
@code{.py}
FLANN_INDEX_LSH = 6
index_params= dict(algorithm = FLANN_INDEX_LSH,
                   table_number = 6, # 12
                   key_size = 12,     # 20
                   multi_probe_level = 1) #2
@endcode
Second dictionary is the SearchParams. It specifies the number of times the trees in the index
should be recursively traversed. Higher values gives better precision, but also takes more time. If
you want to change the value, pass search_params = dict(checks=100).

With this information, we are good to go.
@code{.py}
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

img1 = cv.imread('box.png',cv.IMREAD_GRAYSCALE)          # queryImage
img2 = cv.imread('box_in_scene.png',cv.IMREAD_GRAYSCALE) # trainImage

# Initiate SIFT detector
sift = cv.SIFT_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

# FLANN parameters
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks=50)   # or pass empty dictionary

flann = cv.FlannBasedMatcher(index_params,search_params)

matches = flann.knnMatch(des1,des2,k=2)

# Need to draw only good matches, so create a mask
matchesMask = [[0,0] for i in range(len(matches))]

# ratio test as per Lowe's paper
for i,(m,n) in enumerate(matches):
    if m.distance < 0.7*n.distance:
        matchesMask[i]=[1,0]

draw_params = dict(matchColor = (0,255,0),
                   singlePointColor = (255,0,0),
                   matchesMask = matchesMask,
                   flags = cv.DrawMatchesFlags_DEFAULT)

img3 = cv.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)

plt.imshow(img3,),plt.show()
@endcode
See the result below:

![image](images/matcher_flann.jpg)

---
Source: https://raw.githubusercontent.com/opencv/opencv/4.x/doc/py_tutorials/py_imgproc/py_geometric_transformations/py_geometric_transformations.markdown

Geometric Transformations of Images {#tutorial_py_geometric_transformations}
===================================

Goals
-----

-   Learn to apply different geometric transformations to images, like translation, rotation, affine
    transformation etc.
-   You will see these functions: **cv.getPerspectiveTransform**

Transformations
---------------

OpenCV provides two transformation functions, **cv.warpAffine** and **cv.warpPerspective**, with
which you can perform all kinds of transformations. **cv.warpAffine** takes a 2x3 transformation
matrix while **cv.warpPerspective** takes a 3x3 transformation matrix as input.

### Scaling

Scaling is just resizing of the image. OpenCV comes with a function **cv.resize()** for this
purpose. The size of the image can be specified manually, or you can specify the scaling factor.
Different interpolation methods are used. Preferable interpolation methods are **cv.INTER_AREA**
for shrinking and **cv.INTER_CUBIC** (slow) & **cv.INTER_LINEAR** for zooming. By default,
the interpolation method **cv.INTER_LINEAR** is used for all resizing purposes. You can resize an
input image with either of following methods:
@code{.py}
import numpy as np
import cv2 as cv

img = cv.imread('messi5.jpg')
assert img is not None, "file could not be read, check with os.path.exists()"

res = cv.resize(img,None,fx=2, fy=2, interpolation = cv.INTER_CUBIC)

#OR

height, width = img.shape[:2]
res = cv.resize(img,(2*width, 2*height), interpolation = cv.INTER_CUBIC)
@endcode
### Translation

Translation is the shifting of an object's location. If you know the shift in the (x,y) direction and let it
be \f$(t_x,t_y)\f$, you can create the transformation matrix \f$\textbf{M}\f$ as follows:

\f[M = \begin{bmatrix} 1 & 0 & t_x \\ 0 & 1 & t_y  \end{bmatrix}\f]

You can take make it into a Numpy array of type np.float32 and pass it into the **cv.warpAffine()**
function. See the below example for a shift of (100,50):
@code{.py}
import numpy as np
import cv2 as cv

img = cv.imread('messi5.jpg', cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"
rows,cols = img.shape

M = np.float32([[1,0,100],[0,1,50]])
dst = cv.warpAffine(img,M,(cols,rows))

cv.imshow('img',dst)
cv.waitKey(0)
cv.destroyAllWindows()
@endcode
**warning**

The third argument of the **cv.warpAffine()** function is the size of the output image, which should
be in the form of **(width, height)**. Remember width = number of columns, and height = number of
rows.

See the result below:

![image](images/translation.jpg)

### Rotation

Rotation of an image for an angle \f$\theta\f$ is achieved by the transformation matrix of the form

\f[M = \begin{bmatrix} cos\theta & -sin\theta \\ sin\theta & cos\theta   \end{bmatrix}\f]

But OpenCV provides scaled rotation with adjustable center of rotation so that you can rotate at any
location you prefer. The modified transformation matrix is given by

\f[\begin{bmatrix} \alpha &  \beta & (1- \alpha )  \cdot center.x -  \beta \cdot center.y \\ - \beta &  \alpha &  \beta \cdot center.x + (1- \alpha )  \cdot center.y \end{bmatrix}\f]

where:

\f[\begin{array}{l} \alpha =  scale \cdot \cos \theta , \\ \beta =  scale \cdot \sin \theta \end{array}\f]

To find this transformation matrix, OpenCV provides a function, **cv.getRotationMatrix2D**. Check out the
below example which rotates the image by 90 degree with respect to center without any scaling.
@code{.py}
img = cv.imread('messi5.jpg', cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"
rows,cols = img.shape

# cols-1 and rows-1 are the coordinate limits.
M = cv.getRotationMatrix2D(((cols-1)/2.0,(rows-1)/2.0),90,1)
dst = cv.warpAffine(img,M,(cols,rows))
@endcode
See the result:

![image](images/rotation.jpg)

### Affine Transformation

In affine transformation, all parallel lines in the original image will still be parallel in the
output image. To find the transformation matrix, we need three points from the input image and their
corresponding locations in the output image. Then **cv.getAffineTransform** will create a 2x3 matrix
which is to be passed to **cv.warpAffine**.

Check the below example, and also look at the points I selected (which are marked in green color):
@code{.py}
img = cv.imread('drawing.png')
assert img is not None, "file could not be read, check with os.path.exists()"
rows,cols,ch = img.shape

pts1 = np.float32([[50,50],[200,50],[50,200]])
pts2 = np.float32([[10,100],[200,50],[100,250]])

M = cv.getAffineTransform(pts1,pts2)

dst = cv.warpAffine(img,M,(cols,rows))

plt.subplot(121),plt.imshow(img),plt.title('Input')
plt.subplot(122),plt.imshow(dst),plt.title('Output')
plt.show()
@endcode
See the result:

![image](images/affine.jpg)

### Perspective Transformation

For perspective transformation, you need a 3x3 transformation matrix. Straight lines will remain
straight even after the transformation. To find this transformation matrix, you need 4 points on the
input image and corresponding points on the output image. Among these 4 points, 3 of them should not
be collinear. Then the transformation matrix can be found by the function
**cv.getPerspectiveTransform**. Then apply **cv.warpPerspective** with this 3x3 transformation
matrix.

See the code below:
@code{.py}
img = cv.imread('sudoku.png')
assert img is not None, "file could not be read, check with os.path.exists()"
rows,cols,ch = img.shape

pts1 = np.float32([[56,65],[368,52],[28,387],[389,390]])
pts2 = np.float32([[0,0],[300,0],[0,300],[300,300]])

M = cv.getPerspectiveTransform(pts1,pts2)

dst = cv.warpPerspective(img,M,(300,300))

plt.subplot(121),plt.imshow(img),plt.title('Input')
plt.subplot(122),plt.imshow(dst),plt.title('Output')
plt.show()
@endcode
Result:

![image](images/perspective.jpg)

Additional Resources
--------------------

-#  "Computer Vision: Algorithms and Applications", Richard Szeliski

---
Source: https://raw.githubusercontent.com/opencv/opencv/4.x/doc/py_tutorials/py_imgproc/py_template_matching/py_template_matching.markdown

Template Matching {#tutorial_py_template_matching}
=================

Goals
-----

In this chapter, you will learn
    -   To find objects in an image using Template Matching
    -   You will see these functions : **cv.matchTemplate()**, **cv.minMaxLoc()**

Theory
------

Template Matching is a method for searching and finding the location of a template image in a larger
image. OpenCV comes with a function **cv.matchTemplate()** for this purpose. It simply slides the
template image over the input image (as in 2D convolution) and compares the template and patch of
input image under the template image. Several comparison methods are implemented in OpenCV. (You can
check docs for more details). It returns a grayscale image, where each pixel denotes how much does
the neighbourhood of that pixel match with template.

If input image is of size (WxH) and template image is of size (wxh), output image will have a size
of (W-w+1, H-h+1). Once you got the result, you can use **cv.minMaxLoc()** function to find where
is the maximum/minimum value. Take it as the top-left corner of rectangle and take (w,h) as width
and height of the rectangle. That rectangle is your region of template.

@note If you are using cv.TM_SQDIFF as comparison method, minimum value gives the best match.

Template Matching in OpenCV
---------------------------

Here, as an example, we will search for Messi's face in his photo. So I created a template as below:

![image](images/messi_face.jpg)

We will try all the comparison methods so that we can see how their results look like:
@code{.py}
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread('messi5.jpg', cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"
img2 = img.copy()
template = cv.imread('template.jpg', cv.IMREAD_GRAYSCALE)
assert template is not None, "file could not be read, check with os.path.exists()"
w, h = template.shape[::-1]

# All the 6 methods for comparison in a list
methods = ['TM_CCOEFF', 'TM_CCOEFF_NORMED', 'TM_CCORR',
            'TM_CCORR_NORMED', 'TM_SQDIFF', 'TM_SQDIFF_NORMED']

for meth in methods:
    img = img2.copy()
    method = getattr(cv, meth)

    # Apply template Matching
    res = cv.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    cv.rectangle(img,top_left, bottom_right, 255, 2)

    plt.subplot(121),plt.imshow(res,cmap = 'gray')
    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(img,cmap = 'gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.suptitle(meth)

    plt.show()
@endcode
See the results below:

-   cv.TM_CCOEFF

![image](images/template_ccoeff_1.jpg)

-   cv.TM_CCOEFF_NORMED

![image](images/template_ccoeffn_2.jpg)

-   cv.TM_CCORR

![image](images/template_ccorr_3.jpg)

-   cv.TM_CCORR_NORMED

![image](images/template_ccorrn_4.jpg)

-   cv.TM_SQDIFF

![image](images/template_sqdiff_5.jpg)

-   cv.TM_SQDIFF_NORMED

![image](images/template_sqdiffn_6.jpg)

You can see that the result using **cv.TM_CCORR** is not good as we expected.

Template Matching with Multiple Objects
---------------------------------------

In the previous section, we searched image for Messi's face, which occurs only once in the image.
Suppose you are searching for an object which has multiple occurrences, **cv.minMaxLoc()** won't
give you all the locations. In that case, we will use thresholding. So in this example, we will use
a screenshot of the famous game **Mario** and we will find the coins in it.
@code{.py}
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img_rgb = cv.imread('mario.png')
assert img_rgb is not None, "file could not be read, check with os.path.exists()"
img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
template = cv.imread('mario_coin.png', cv.IMREAD_GRAYSCALE)
assert template is not None, "file could not be read, check with os.path.exists()"
w, h = template.shape[::-1]

res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
    cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

cv.imwrite('res.png',img_rgb)
@endcode
Result:

![image](images/res_mario.jpg)
