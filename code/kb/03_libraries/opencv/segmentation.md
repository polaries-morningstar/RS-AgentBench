# OpenCV Segmentation: Watershed & GrabCut

Source: https://raw.githubusercontent.com/opencv/opencv/4.x/doc/py_tutorials/py_imgproc/py_watershed/py_watershed.markdown
Source: https://raw.githubusercontent.com/opencv/opencv/4.x/doc/py_tutorials/py_imgproc/py_grabcut/py_grabcut.markdown

Image Segmentation with Watershed Algorithm {#tutorial_py_watershed}
===========================================

Goal
----

In this chapter,
    -   We will learn to use marker-based image segmentation using watershed algorithm
    -   We will see: **cv.watershed()**

Theory
------

Any grayscale image can be viewed as a topographic surface where high intensity denotes peaks and
hills while low intensity denotes valleys. You start filling every isolated valleys (local minima)
with different colored water (labels). As the water rises, depending on the peaks (gradients)
nearby, water from different valleys, obviously with different colors will start to merge. To avoid
that, you build barriers in the locations where water merges. You continue the work of filling water
and building barriers until all the peaks are under water. Then the barriers you created gives you
the segmentation result. This is the "philosophy" behind the watershed. You can visit the [CMM
webpage on watershed](https://people.cmm.minesparis.psl.eu/users/beucher/wtshed.html) to understand it with the help of
some animations.

But this approach gives you oversegmented result due to noise or any other irregularities in the
image. So OpenCV implemented a marker-based watershed algorithm where you specify which are all
valley points are to be merged and which are not. It is an interactive image segmentation. What we
do is to give different labels for our object we know. Label the region which we are sure of being
the foreground or object with one color (or intensity), label the region which we are sure of being
background or non-object with another color and finally the region which we are not sure of
anything, label it with 0. That is our marker. Then apply watershed algorithm. Then our marker will
be updated with the labels we gave, and the boundaries of objects will have a value of -1.

Code
----

Below we will see an example on how to use the Distance Transform along with watershed to segment
mutually touching objects.

Consider the coins image below, the coins are touching each other. Even if you threshold it, it will
be touching each other.

![image](images/water_coins.jpg)

We start with finding an approximate estimate of the coins. For that, we can use the Otsu's
binarization.
@code{.py}
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

img = cv.imread('coins.png')
assert img is not None, "file could not be read, check with os.path.exists()"
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(gray,0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
@endcode
Result:

![image](images/water_thresh.jpg)

Now we need to remove any small white noises in the image. For that we can use morphological
opening. To remove any small holes in the object, we can use morphological closing. So, now we know
for sure that region near to center of objects are foreground and region much away from the object
are background. Only region we are not sure is the boundary region of coins.

So we need to extract the area which we are sure they are coins. Erosion removes the boundary
pixels. So whatever remaining, we can be sure it is coin. That would work if objects were not
touching each other. But since they are touching each other, another good option would be to find
the distance transform and apply a proper threshold. Next we need to find the area which we are sure
they are not coins. For that, we dilate the result. Dilation increases object boundary to
background. This way, we can make sure whatever region in background in result is really a
background, since boundary region is removed. See the image below.

![image](images/water_fgbg.jpg)

The remaining regions are those which we don't have any idea, whether it is coins or background.
Watershed algorithm should find it. These areas are normally around the boundaries of coins where
foreground and background meet (Or even two different coins meet). We call it border. It can be
obtained from subtracting sure_fg area from sure_bg area.
@code{.py}
# noise removal
kernel = np.ones((3,3),np.uint8)
opening = cv.morphologyEx(thresh,cv.MORPH_OPEN,kernel, iterations = 2)

# sure background area
sure_bg = cv.dilate(opening,kernel,iterations=3)

# Finding sure foreground area
dist_transform = cv.distanceTransform(opening,cv.DIST_L2,5)
ret, sure_fg = cv.threshold(dist_transform,0.7*dist_transform.max(),255,0)

# Finding unknown region
sure_fg = np.uint8(sure_fg)
unknown = cv.subtract(sure_bg,sure_fg)
@endcode
See the result. In the thresholded image, we get some regions of coins which we are sure of coins
and they are detached now. (In some cases, you may be interested in only foreground segmentation,
not in separating the mutually touching objects. In that case, you need not use distance transform,
just erosion is sufficient. Erosion is just another method to extract sure foreground area, that's
all.)

![image](images/water_dt.jpg)

Now we know for sure which are region of coins, which are background and all. So we create marker
(it is an array of same size as that of original image, but with int32 datatype) and label the
regions inside it. The regions we know for sure (whether foreground or background) are labelled with
any positive integers, but different integers, and the area we don't know for sure are just left as
zero. For this we use **cv.connectedComponents()**. It labels background of the image with 0, then
other objects are labelled with integers starting from 1.

But we know that if background is marked with 0, watershed will consider it as unknown area. So we
want to mark it with different integer. Instead, we will mark unknown region, defined by unknown,
with 0.
@code{.py}
# Marker labelling
ret, markers = cv.connectedComponents(sure_fg)

# Add one to all labels so that sure background is not 0, but 1
markers = markers+1

# Now, mark the region of unknown with zero
markers[unknown==255] = 0
@endcode
See the result shown in JET colormap. The dark blue region shows unknown region. Sure coins are
colored with different values. Remaining area which are sure background are shown in lighter blue
compared to unknown region.

![image](images/water_marker.jpg)

Now our marker is ready. It is time for final step, apply watershed. Then marker image will be
modified. The boundary region will be marked with -1.
@code{.py}
markers = cv.watershed(img,markers)
img[markers == -1] = [255,0,0]
@endcode
See the result below. For some coins, the region where they touch are segmented properly and for
some, they are not.

![image](images/water_result.jpg)

Additional Resources
--------------------

-#  CMM page on [Watershed Transformation](https://people.cmm.minesparis.psl.eu/users/beucher/wtshed.html)

Exercises
---------

-#  OpenCV samples has an interactive sample on watershed segmentation, watershed.py. Run it, Enjoy
    it, then learn it.

---

Interactive Foreground Extraction using GrabCut Algorithm {#tutorial_py_grabcut}
=========================================================

Goal
----

In this chapter
    -   We will see GrabCut algorithm to extract foreground in images
    -   We will create an interactive application for this.

Theory
------

GrabCut algorithm was designed by Carsten Rother, Vladimir Kolmogorov & Andrew Blake from Microsoft
Research Cambridge, UK. in their paper, ["GrabCut": interactive foreground extraction using iterated
graph cuts](http://dl.acm.org/citation.cfm?id=1015720) . An algorithm was needed for foreground
extraction with minimal user interaction, and the result was GrabCut.

How it works from user point of view ? Initially user draws a rectangle around the foreground region
(foreground region should be completely inside the rectangle). Then algorithm segments it
iteratively to get the best result. Done. But in some cases, the segmentation won't be fine, like,
it may have marked some foreground region as background and vice versa. In that case, user need to
do fine touch-ups. Just give some strokes on the images where some faulty results are there. Strokes
basically says *"Hey, this region should be foreground, you marked it background, correct it in next
iteration"* or its opposite for background. Then in the next iteration, you get better results.

See the image below. First player and football is enclosed in a blue rectangle. Then some final
touchups with white strokes (denoting foreground) and black strokes (denoting background) is made.
And we get a nice result.

![image](images/grabcut_output1.jpg)

So what happens in background ?

-   User inputs the rectangle. Everything outside this rectangle will be taken as sure background
    (That is the reason it is mentioned before that your rectangle should include all the
    objects). Everything inside rectangle is unknown. Similarly any user input specifying
    foreground and background are considered as hard-labelling which means they won't change in
    the process.
-   Computer does an initial labelling depending on the data we gave. It labels the foreground and
    background pixels (or it hard-labels)
-   Now a Gaussian Mixture Model(GMM) is used to model the foreground and background.
-   Depending on the data we gave, GMM learns and create new pixel distribution. That is, the
    unknown pixels are labelled either probable foreground or probable background depending on its
    relation with the other hard-labelled pixels in terms of color statistics (It is just like
    clustering).
-   A graph is built from this pixel distribution. Nodes in the graphs are pixels. Additional two
    nodes are added, **Source node** and **Sink node**. Every foreground pixel is connected to
    Source node and every background pixel is connected to Sink node.
-   The weights of edges connecting pixels to source node/end node are defined by the probability
    of a pixel being foreground/background. The weights between the pixels are defined by the edge
    information or pixel similarity. If there is a large difference in pixel color, the edge
    between them will get a low weight.
-   Then a mincut algorithm is used to segment the graph. It cuts the graph into two separating
    source node and sink node with minimum cost function. The cost function is the sum of all
    weights of the edges that are cut. After the cut, all the pixels connected to Source node
    become foreground and those connected to Sink node become background.
-   The process is continued until the classification converges.

It is illustrated in below image (Image Courtesy: <http://www.cs.ru.ac.za/research/g02m1682/>)

![image](images/grabcut_scheme.jpg)

Demo
----

Now we go for grabcut algorithm with OpenCV. OpenCV has the function, **cv.grabCut()** for this. We
will see its arguments first:

-   *img* - Input image
-   *mask* - It is a mask image where we specify which areas are background, foreground or
    probable background/foreground etc. It is done by the following flags, **cv.GC_BGD,
    cv.GC_FGD, cv.GC_PR_BGD, cv.GC_PR_FGD**, or simply pass 0,1,2,3 to image.
-   *rect* - It is the coordinates of a rectangle which includes the foreground object in the
    format (x,y,w,h)
-   *bdgModel*, *fgdModel* - These are arrays used by the algorithm internally. You just create
    two np.float64 type zero arrays of size (1,65).
-   *iterCount* - Number of iterations the algorithm should run.
-   *mode* - It should be **cv.GC_INIT_WITH_RECT** or **cv.GC_INIT_WITH_MASK** or combined
    which decides whether we are drawing rectangle or final touchup strokes.

First let's see with rectangular mode. We load the image, create a similar mask image. We create
*fgdModel* and *bgdModel*. We give the rectangle parameters. It's all straight-forward. Let the
algorithm run for 5 iterations. Mode should be *cv.GC_INIT_WITH_RECT* since we are using
rectangle. Then run the grabcut. It modifies the mask image. In the new mask image, pixels will be
marked with four flags denoting background/foreground as specified above. So we modify the mask such
that all 0-pixels and 2-pixels are put to 0 (ie background) and all 1-pixels and 3-pixels are put to
1(ie foreground pixels). Now our final mask is ready. Just multiply it with input image to get the
segmented image.
@code{.py}
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

img = cv.imread('messi5.jpg')
assert img is not None, "file could not be read, check with os.path.exists()"
mask = np.zeros(img.shape[:2],np.uint8)

bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)

rect = (50,50,450,290)
cv.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv.GC_INIT_WITH_RECT)

mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
img = img*mask2[:,:,np.newaxis]

plt.imshow(img),plt.colorbar(),plt.show()
@endcode
See the results below:

![image](images/grabcut_rect.jpg)

Oops, Messi's hair is gone. *Who likes Messi without his hair?* We need to bring it back. So we will
give there a fine touchup with 1-pixel (sure foreground). At the same time, Some part of ground has
come to picture which we don't want, and also some logo. We need to remove them. There we give some
0-pixel touchup (sure background). So we modify our resulting mask in previous case as we told now.

*What I actually did is that, I opened input image in paint application and added another layer to
the image. Using brush tool in the paint, I marked missed foreground (hair, shoes, ball etc) with
white and unwanted background (like logo, ground etc) with black on this new layer. Then filled
remaining background with gray. Then loaded that mask image in OpenCV, edited original mask image we
got with corresponding values in newly added mask image. Check the code below:*
@code{.py}
# newmask is the mask image I manually labelled
newmask = cv.imread('newmask.png', cv.IMREAD_GRAYSCALE)
assert newmask is not None, "file could not be read, check with os.path.exists()"

# wherever it is marked white (sure foreground), change mask=1
# wherever it is marked black (sure background), change mask=0
mask[newmask == 0] = 0
mask[newmask == 255] = 1

mask, bgdModel, fgdModel = cv.grabCut(img,mask,None,bgdModel,fgdModel,5,cv.GC_INIT_WITH_MASK)

mask = np.where((mask==2)|(mask==0),0,1).astype('uint8')
img = img*mask[:,:,np.newaxis]
plt.imshow(img),plt.colorbar(),plt.show()
@endcode
See the result below:

![image](images/grabcut_mask.jpg)

So that's it. Here instead of initializing in rect mode, you can directly go into mask mode. Just
mark the rectangle area in mask image with 2-pixel or 3-pixel (probable background/foreground). Then
mark our sure_foreground with 1-pixel as we did in second example. Then directly apply the grabCut
function with mask mode.

Exercises
---------

-#  OpenCV samples contain a sample grabcut.py which is an interactive tool using grabcut. Check it.
    Also watch this [youtube video](http://www.youtube.com/watch?v=kAwxLTDDAwU) on how to use it.
-#  Here, you can make this into a interactive sample with drawing rectangle and strokes with mouse,
    create trackbar to adjust stroke width etc.
