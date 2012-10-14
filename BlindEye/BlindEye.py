#!/usr/bin/python


from hsvVals_MouseClick import hsvVals_MouseClick as hi
from color_detector import colorThresholdDetector as ct

myhi = hi()
myct = ct() 

print myct.manageRange(myhi.getHsvRange())


