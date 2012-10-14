#!/usr/bin/python


from hsvVals_MouseClick import hsvVals_MouseClick as hi
from color_detector import colorThresholdDetector as ct
from Centerify import Centerify

myhi = hi()
myct = ct() 
thresholds = myct.manageRange(myhi.getHsvRange())
MyCenterify = Centerify(thresholds[0],thresholds[1])






