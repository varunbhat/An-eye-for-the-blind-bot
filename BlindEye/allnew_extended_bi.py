#!/usr/bin/python


import cv
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-c", "--camera", dest="camera_device", default=0,
                    help="the index of your camera. if /dev/videoN is your camera device, then --camera=N [default: %default]")
parser.add_option("-m", "--min-threshold", dest="min_threshold",
                    default="(70, 110, 120)",
                    help="minimum threshold value in HSV (hue,sat,val). if not given, will track a blue object. [default: %default]")
parser.add_option("-x", "--max-threshold", dest="max_threshold",
                    default="(105, 255, 255)",
                    help="maximum threshold value in HSV (hue,sat,val). if not given, will track a blue object. [default: %default]")
parser.add_option("-s", "--smoothness", dest="smoothness", default=4,
                    help="how many previous positions to interpolate to find our current position. higher smoothness => slower tracking, but less jerkiness [default: %default]")

(options, args) = parser.parse_args()
MY_CAMERA = int(options.camera_device)
SMOOTHNESS = int(options.smoothness)
MIN_THRESH = eval(options.min_threshold)
MAX_THRESH = eval(options.max_threshold)



def thresholded_image(image):

    image_hsv = cv.CreateImage(cv.GetSize(image), image.depth, 3)
    cv.CvtColor(image, image_hsv, cv.CV_BGR2HSV)

    image_threshed = cv.CreateImage(cv.GetSize(image), image.depth, 1)
    cv.InRangeS(image_hsv, MIN_THRESH, MAX_THRESH, image_threshed)

    return image_threshed


capture = cv.CaptureFromCAM(MY_CAMERA)
if not capture:
    print "I am blinded, check Camera Config"
    exit(1)


cv.NamedWindow('camera', cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow('threshed', cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow('cropped', cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow('camera feed', cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow('filtered feed', cv.CV_WINDOW_AUTOSIZE)

# initialize position array
positions_x, positions_y = [0]*SMOOTHNESS, [0]*SMOOTHNESS


while 1:    
    image = cv.QueryFrame(capture)
#    image = cv.LoadImage("2012_automata.jpg")
    if not image:
        break

#    Blurring image
    image_smoothed = cv.CloneImage(image)
    cv.Smooth(image, image_smoothed, cv.CV_GAUSSIAN, 1)


    image_threshed = thresholded_image(image_smoothed)
    
    cv.Dilate(image_threshed, image_threshed, None, 3)
    cv.Erode(image_threshed, image_threshed, None, 3)

    blobContour = None

#    Contour Finding !!!!!!!!!Main Algo!!!!!!!!
    current_contour = cv.FindContours(cv.CloneImage(image_threshed), cv.CreateMemStorage(), cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
    #just making an outline
    cv.DrawContours(image, current_contour,(0,0,255),(0,100,100),4)

    if len(current_contour) != 0:

        largest_contour = current_contour
        while True:
            current_contour = current_contour.h_next()
            if (not current_contour):
                break
            if (cv.ContourArea(current_contour) > cv.ContourArea(largest_contour)):
                largest_contour = current_contour


        # if we got a good enough blob
        if cv.ContourArea(largest_contour)>2.0:
            blobContour = largest_contour
            # find the center of the blob
            moments = cv.Moments(largest_contour, 1)
            positions_x.append(cv.GetSpatialMoment(moments, 1, 0)/cv.GetSpatialMoment(moments, 0, 0))
            positions_y.append(cv.GetSpatialMoment(moments, 0, 1)/cv.GetSpatialMoment(moments, 0, 0))
            # discard all but the last N positions
            positions_x, positions_y = positions_x[-SMOOTHNESS:], positions_y[-SMOOTHNESS:]
            cv.DrawContours(image_threshed, largest_contour, cv.RGB(60, 60, 60), cv.RGB(60, 60, 60),1,-1)
    
    object_indicator = cv.CreateImage(cv.GetSize(image), image.depth, 3)

    pos_x = (sum(positions_x)/len(positions_x))
    pos_y = (sum(positions_y)/len(positions_y))
    object_position = (int(pos_x),int(pos_y))
#    print pos_x , pos_y

    cv.Circle(object_indicator, object_position, 12, (0,0,255), 4)

    cropped = cv.CreateImage((image_threshed.width,image_threshed.height), image_threshed.depth, image_threshed.nChannels)
    src_region = cv.GetSubRect(image_threshed, (0,int(pos_y)-(2/100),image_threshed.width,image_threshed.height*3/100))
    
    

    # show the images
    cv.Add(image, object_indicator, image)
    cv.ShowImage('threshed', image_threshed)
    cv.ShowImage('camera', image)
    cv.ShowImage('cropped', src_region)

    # break from the loop if there is a key press
    c = cv.WaitKey(10)
    if c != -1:
        break

