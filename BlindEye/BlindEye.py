#!/usr/bin/python

import cv
from hsvVals_MouseClick import hsvVals_MouseClick as hi
from color_detector import colorThresholdDetector as ct
from Centerify import Centerify


myhi = hi()
myct = ct() 
thresholds = myct.manageRange(myhi.getHsvRange())
MyCenterify = Centerify(thresholds[0],thresholds[1])
MyCenterify.doStuff()
#print type(slicedImage)
#contourx = MyCenterify.getContour(slicedImage)

#if cv.ContourArea(contourx)> 2:
#    centers = []
#    for i in range(len(contourx)):
#        centers.append(MyCenterify.contourCenter(contourx, 4))
#        contourx = contourx.h_next()
#    for i in range(len(contourx)):
#        MyCenterify.drawPointOnImage(slicedImage, centers[i])
#cv.NamedWindow('camera', cv.CV_WINDOW_AUTOSIZE)
#cv.ShowImage('points', slicedImage)
#cv.WaitKey(10000);
