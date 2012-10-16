#!/usr/bin/python

import cv

class Centerify:
    def __init__(self,mint,maxt):
        self.MY_CAMERA = 1 
        self.SMOOTHNESS = 4
        self.MIN_THRESH =mint
        self.MAX_THRESH =maxt
#        self.doStuff()

    def thresholded_image(self,image):
        image_hsv = cv.CreateImage(cv.GetSize(image), image.depth, 3)
        cv.CvtColor(image, image_hsv, cv.CV_BGR2HSV)
    
        image_threshed = cv.CreateImage(cv.GetSize(image), image.depth, 1)
        cv.InRangeS(image_hsv, self.MIN_THRESH, self.MAX_THRESH, image_threshed)
    
        return image_threshed

    def doStuff(self):
        capture = cv.CaptureFromCAM(self.MY_CAMERA)
        if not capture:
            print "I am blinded, check Camera Config"
            exit(1)

        cv.NamedWindow('camera', cv.CV_WINDOW_AUTOSIZE)
        cv.NamedWindow('threshed', cv.CV_WINDOW_AUTOSIZE)
#        cv.NamedWindow('cropped', cv.CV_WINDOW_AUTOSIZE)

        while 1:    
            image = cv.QueryFrame(capture)
#            image = cv.LoadImage("2012_automata.jpg")
            if not image:
                break
        
#/////////////////////////////////////////////////////
#            Blurring my image and doing stuff
            image_smoothed = cv.CloneImage(image)
            cv.Smooth(image, image_smoothed, cv.CV_GAUSSIAN, 1)
            image_threshed = self.thresholded_image(image_smoothed)
            cv.Dilate(image_threshed, image_threshed, None, 3)
            cv.Erode(image_threshed, image_threshed, None, 3)
#///////////////////////////////////////////////////////
#            Get the Contours
            current_contour = cv.FindContours(cv.CloneImage(image_threshed), cv.CreateMemStorage(), cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
            object_position=(0,0)
            if len(current_contour) != 0:
                object_position =  self.contourCenter(self.largestContour(current_contour))

#            cropped = cv.CreateImage((image_threshed.width,image_threshed.height), image_threshed.depth, image_threshed.nChannels)
#            print object_position
#            try:
#                src_region = cv.GetSubRect(image_threshed, (0,object_position[1]-(2/100),image_threshed.width,image_threshed.height*3/100))
#            except:
#                src_region = cv.GetSubRect(image_threshed, (0,0,image_threshed.width,image_threshed.height*5/100))
            image = self.drawPointOnImage(image, object_position)
#            image = self.getSlicedCenter(src_region, image)
            image = self.getSlicedCenter(image_threshed, image)
            cv.ShowImage('threshed', image_threshed)
            cv.ShowImage('camera', image)
            
#            cv.ShowImage('cropped', src_region)
            c = cv.WaitKey(10)
            if c != -1:
#                return src_region
                break
    
    def contourCenter(self,thisContour,smoothness=4): 
        positions_x, positions_y = [0]*smoothness, [0]*smoothness 
#        print type(thisContour)
        if cv.ContourArea(thisContour)>2.0:
            moments = cv.Moments(thisContour, 1)
            positions_x.append(cv.GetSpatialMoment(moments, 1, 0)/cv.GetSpatialMoment(moments, 0, 0))
            positions_y.append(cv.GetSpatialMoment(moments, 0, 1)/cv.GetSpatialMoment(moments, 0, 0))
            positions_x, positions_y = positions_x[-self.SMOOTHNESS:], positions_y[-self.SMOOTHNESS:]
            pos_x = (sum(positions_x)/len(positions_x))
            pos_y = (sum(positions_y)/len(positions_y))
            return (int(pos_x*smoothness),int(pos_y*smoothness))
        
    def largestContour(self,contourCluster):
        if len(contourCluster) != 0:
            largest_contour = contourCluster
            while True:
                contourCluster = contourCluster.h_next()
                if (not contourCluster):
#                    print type(largest_contour)
                    return largest_contour
#                    break
                if (cv.ContourArea(contourCluster) > cv.ContourArea(largest_contour)):
                    largest_contour = contourCluster

    def drawPointOnImage(self,img,object_position):
        try:
            object_indicator = cv.CreateImage(cv.GetSize(img), img.depth, 3)
            cv.Circle(object_indicator, object_position, 12, (0,0,255), 4)
            cv.Add(img, object_indicator, img)
        except:
            pass
#            object_indicator = cv.CreateImage(cv.GetSize(img), img.depth, 1)
#            cv.Circle(object_indicator, object_position, 12, (0), 4)
#            cv.Add(img, object_indicator, img)
        return img
    def getContour(self,image):
        current_contour = cv.FindContours(cv.CloneImage(image), cv.CreateMemStorage(), cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
        return  current_contour
    def getSlicedCenter(self,src_region,image):
        centers = []
#        src_region = cv.iplimage(src_region)
        contourx = cv.FindContours(src_region, cv.CreateMemStorage(), cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
#        print len(contourx)
        if cv.ContourArea(contourx)> 2:
            for i in range(len(contourx)):
                if contourx:
                    centers.append(self.contourCenter(contourx, 4))
                    contourx = contourx.h_next()

            for i in range(len(centers)):
                self.drawPointOnImage(image, centers[i])
            print centers
            image = self.pointTheBlackAndWhite(image,centers)
        return image
    
#    def aimAtThePoint(self):
    def pointTheBlackAndWhite(self,image,centers):
        for i in centers:
            image = self.drawPointOnImage(image, i)
        return image