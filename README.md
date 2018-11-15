# find_shape_center
using opencv find center of shapes mainly for circle and ellipse  
## Method (3 type)
1. Using edge detection to find the contours of the shape and then calculate the moment which we use to find the center of the shape.  
    * We can detect not only circle and ellipse but any shape we meet.
2. Using Hough transform to find the circle and then we can get the center of the circle.
    * It's not applicable and accurate to detect ellipse
3. Using idea of PCA to project points onto the two axes and then calculate the intersection of the two axes to find the center.
    * It's applicable to detect both circle and ellipse, but when the slope of one axe is equal to 0, some problems may occur.
  
## Code
The three methods above are implement by python
