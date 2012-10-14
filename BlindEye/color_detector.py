#!/usr/bin/python

import cv

class colorThresholdDetector:
    def thresholded_image(self,image, thresh_min, thresh_max):
        
        image_hsv = cv.CreateImage(cv.GetSize(image), image.depth, 3)
        cv.CvtColor(image, image_hsv, cv.CV_BGR2HSV)
        
        image_threshed = cv.CreateImage(cv.GetSize(image), image.depth, 1)
        cv.InRangeS(image_hsv, thresh_min, thresh_max, image_threshed)
        return image_threshed
    
    def manageRange(self,hsvs):
        self.MY_CAMERA = int(1)
        cv.NamedWindow('camera feed', cv.CV_WINDOW_AUTOSIZE)
        cv.NamedWindow('filtered feed', cv.CV_WINDOW_AUTOSIZE)
        
        capture = cv.CaptureFromCAM(self.MY_CAMERA)
        if not capture:
            print "Could not initialize camera feed!"
            exit(1)
        
        # initial thresholds
        hue = hsvs[0]
        hue_range = 50
        sat = hsvs[1]
        sat_range = 100
        val = hsvs[2]
        val_range = 100
        thresh_min = cv.Scalar(hue-hue_range/2.0, sat-sat_range/2.0, val-val_range/2.0)
        thresh_max = cv.Scalar(hue+hue_range/2.0, sat+sat_range/2.0, val+val_range/2.0)
        
        
        while 1:    
            image = cv.QueryFrame(capture)
#            image = cv.LoadImage('2012_automata.jpg')
            if not image:
                print "Could not query image"
                break
        
            # filter the image
            image_threshed = self.thresholded_image(image, thresh_min, thresh_max)

            cv.ShowImage('camera feed', image)
            cv.ShowImage('filtered feed', image_threshed) 
        
            # break from the loop if there is a key press
            c = cv.WaitKey(1)
            if c == 27 or c == 1048603:
                print (thresh_min,thresh_max)
                
                break
            elif c == -1:
                continue
        
            if c == 101 or c == 1048677:
                hue += 1
            elif c == 120 or c == 1048696:
                hue -= 1
            elif c == 100 or c == 1048676:
                hue_range += 1
            elif c == 115 or c == 1048691:
                hue_range -= 1
            elif c == 116 or c == 1048692:
                sat += 1
            elif c == 118 or c == 1048694:
                sat -= 1
            elif c == 103 or c == 1048679:
                sat_range += 1
            elif c == 102 or c == 1048678:
                sat_range -= 1
            elif c == 117 or c == 1048693:
                val += 1
            elif c == 110 or c == 1048686:
                val -= 1
            elif c == 106 or c == 11111111:
                val_range += 1
            elif c == 104 or c == 1048680:
                val_range -= 1
            else:
                print "key %s" % c
                continue
        
            thresh_min = cv.Scalar(hue-hue_range/2.0, sat-sat_range/2.0, val-val_range/2.0)
            thresh_max = cv.Scalar(hue+hue_range/2.0, sat+sat_range/2.0, val+val_range/2.0)
            print "(h,s,v):\n\tmin=%s\n\tmax=%s"%(thresh_min,thresh_max)
    
