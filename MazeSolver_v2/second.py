import cv

import Image


def thresholded_image(image, min_treshold, max_treshold):
    image_hsv = cv.CreateImage(cv.GetSize(image), image.depth, 3)
    cv.CvtColor(image, image_hsv, cv.CV_BGR2HSV)
    image_threshed = cv.CreateImage(cv.GetSize(image), image.depth, 1)
    cv.InRangeS(image_hsv, min_treshold, max_treshold, image_threshed)
    return image_threshed

def hsv_image(image):
    hsv = cv.CreateImage(cv.GetSize(image), image.depth, 3)
    cv.CvtColor(image, hsv, cv.CV_BGR2HSV)
    return hsv


def getMinMaxTreshold(arrayOfTreshold):
    if len(arrayOfTreshold) > 0:
        min = list(arrayOfTreshold[0])
        max = list(arrayOfTreshold[0])
        for i in range(4):
            for j in range(len(arrayOfTreshold)):
                if arrayOfTreshold[j][i] < min[i]:
                    min[i] = arrayOfTreshold[j][i] - 1
                if arrayOfTreshold[j][i] > max[i]:
                    max[i] = arrayOfTreshold[j][i] + 1
        print (min, max)
        return (min, max)
    else:
        return ([0, 0, 0, 0], [0, 0, 0, 0])
                
def setTreshold(event, x, y, flag, param):
    if(event == cv.CV_EVENT_LBUTTONDOWN):
        s = cv.Get2D(hsvImg, x , y)
        thresholdrange.append(s)
        temp = getMinMaxTreshold(thresholdrange)
        imageTreshold = thresholded_image(image, temp[0], temp[1])
        cv.ShowImage('threshold', imageTreshold)


def contourCenter(thisContour, smoothness=4): 
    positions_x, positions_y = [0] * smoothness, [0] * smoothness 
    if cv.ContourArea(thisContour) > 2.0:
        moments = cv.Moments(thisContour, 1)
        positions_x.append(cv.GetSpatialMoment(moments, 1, 0) / cv.GetSpatialMoment(moments, 0, 0))
        positions_y.append(cv.GetSpatialMoment(moments, 0, 1) / cv.GetSpatialMoment(moments, 0, 0))
        positions_x, positions_y = positions_x[-smoothness:], positions_y[-smoothness:]
        pos_x = (sum(positions_x) / len(positions_x))
        pos_y = (sum(positions_y) / len(positions_y))
        return (int(pos_x * smoothness), int(pos_y * smoothness))

def largestContour(contourCluster):
#    print len(contourCluster)
    if len(contourCluster) != 0:
        largest_contour = contourCluster
        while True:
            contourCluster = contourCluster.h_next()
            if (not contourCluster):
                return largest_contour
            if (cv.ContourArea(contourCluster) > cv.ContourArea(largest_contour)):
                largest_contour = contourCluster
def getSlicedCenter(contourCluster):
    centerArr = []
    
    if len(contourCluster) != 0:
        while True:
#            print cv.ContourArea(contourCluster)

            x = contourCenter(contourCluster)
            if x != None  :
#                if  (cv.ContourArea(contourCluster) > 20):
                    centerArr.append(contourCenter(contourCluster))
            contourCluster = contourCluster.h_next()
            if (not contourCluster):
                return centerArr








initialRotate = 30
cv.NamedWindow('camera', cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow('threshold', cv.CV_WINDOW_AUTOSIZE)
capture = cv.CaptureFromCAM(0)
 

#image = cv.QueryFrame(capture)
image = cv.LoadImage('2012_automata_1.png')
imageCopy = cv.CloneImage(image)
imageTreshold = thresholded_image(image, (0, 0, 0, 0), (0, 0, 0, 0))
dialatecount = 0
thresholdrange = []
hsvImg = hsv_image(image)
cv.ShowImage("camera", image)
cv.ShowImage('threshold', imageTreshold)

while 1:
    cv.SetMouseCallback("camera", setTreshold, 0);
    keyPressed = cv.WaitKey(10000)
    if keyPressed == 27:
        break
    elif keyPressed == -1:
        pass
    elif keyPressed == 114:
        imageTreshold = thresholded_image(image, (0, 0, 0, 0), (0, 0, 0, 0))
        thresholdrange = []
        temp = getMinMaxTreshold(thresholdrange)
        imageTreshold = thresholded_image(image, temp[0], temp[1])
        cv.ShowImage('threshold', imageTreshold)
    elif keyPressed == 100:
        dialatecount = dialatecount + 1
        temp = getMinMaxTreshold(thresholdrange)
        imageTreshold = thresholded_image(image, temp[0], temp[1])
        cv.Dilate(imageTreshold, imageTreshold, None, dialatecount)
        cv.ShowImage('threshold', imageTreshold)
    elif keyPressed == 101:
        temp = getMinMaxTreshold(thresholdrange)
        imageTreshold = thresholded_image(image, temp[0], temp[1])
        cv.Erode(imageTreshold, imageTreshold, None, 1)
#        cv.Erode(imageTreshold, imageTreshold, None, 10)
        cv.ShowImage('threshold', imageTreshold)
    else:
        print keyPressed



current_contour = cv.FindContours(cv.CloneImage(imageTreshold), cv.CreateMemStorage(), cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
object_position = (0, 0)
if len(current_contour) != 0:
    object_position = contourCenter(largestContour(current_contour))



minSizeofImage = min([image.width - object_position[0], object_position[0], object_position[1], image.height - object_position[1]])

f = open('ThingsDone.txt', 'w')
f.write("thresholdofarena:" + str(getMinMaxTreshold(thresholdrange)) + '\n')
f.write("dialate:" + str(dialatecount)+'\n')
f.write("center:" + str(object_position)+'\n')
f.write('imagesizeby2:'+str(minSizeofImage)+'\n')



imageTreshold = cv.GetSubRect(imageTreshold, (object_position[0] - minSizeofImage, object_position[1] - minSizeofImage, minSizeofImage * 2, minSizeofImage * 2))
cv.SaveImage("thresholdimg.jpg", imageTreshold)
pi = Image.open("thresholdimg.jpg")

f = open("finalEquation.txt",'w');


for i in range(1, 7):
    deg = 60 * i
    rotated = pi.rotate(initialRotate + deg)
    imageTreshold = cv.CreateImageHeader(rotated.size, cv.IPL_DEPTH_8U, 1)
    cv.SetData(imageTreshold, rotated.tostring())
    imageTreshold = cv.GetSubRect(imageTreshold, (0, minSizeofImage - int(minSizeofImage * .02), 2 * minSizeofImage, int(minSizeofImage * 2 * 1 / 100)))
    slice = cv.CreateImage((imageTreshold.width, imageTreshold.height), 8, 1)
    cv.SaveImage(str(i)+'.jpg',imageTreshold)
    cv.Copy(imageTreshold, slice)
    current_contour = cv.FindContours(cv.CloneImage(slice), cv.CreateMemStorage(), cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
    centerlist = getSlicedCenter(current_contour)
#    print centerlist
    
    difflistfromCenter = []
    
#    difflistbetweenspaces = []
    for j in range(len(centerlist)-1):
        difflistfromCenter.append(abs(centerlist[j+1][0]-centerlist[j][0] ))
#    print difflistfromCenter
    temp_min = min(difflistfromCenter)
    temp_max = max(difflistfromCenter)
    threshx = (temp_min+temp_max)/2
    

    gapBin=[]
    for j in range(3):
        if difflistfromCenter[j] < threshx:
            gapBin.append(0)
        else:
            gapBin.append(1)
    print gapBin
    
    f = open("finalEquation.txt",'a');
    
    f.write(str(gapBin[0]) +' ' +str(gapBin[1])+' ' +str(gapBin[2])+'\n')
#
#    
#    for j in range(len(difflistfromCenter) - 1):
#        difflistbetweenspaces.append(abs(difflistfromCenter[j + 1] - difflistfromCenter[j]))
#    print difflistbetweenspaces
#    for j in range(len(difflistfromCenter) - 1):
#        difflistbetweenspaces.append(abs(difflistfromCenter[j + 1] - difflistfromCenter[j]))
#    print difflistbetweenspaces



