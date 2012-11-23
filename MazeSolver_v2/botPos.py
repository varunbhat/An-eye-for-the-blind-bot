import cv
import math
import serial



tilt = 0

PORT = 0


capture = cv.CaptureFromCAM(0)
f = open('ThingsDone.txt', 'r')
data = f.read()
data = data.split('\n')
data = data[3].split(':')
center = data[1]


def getBotCoord():
    image = cv.QueryFrame(capture)
    imageTreshold = thresholded_image(image, botTreshold[0], botTreshold[1])
    current_contour = cv.FindContours(cv.CloneImage(imageTreshold), cv.CreateMemStorage(), cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
    mypos = (0, 0)
    if len(current_contour) != 0:
        mypos = contourCenter(largestContour(current_contour))
    imagehsv = hsv_image(image)
    s = cv.Get2D(imagehsv, mypos[0] , mypos[1])
    return (mypos, s)


def thresholded_image(image, min_treshold, max_treshold):
    image_hsv = cv.CreateImage(cv.GetSize(image), image.depth, 3)
    cv.CvtColor(image, image_hsv, cv.CV_BGR2HSV)
    image_threshed = cv.CreateImage(cv.GetSize(image), image.depth, 1)
    cv.InRangeS(image_hsv, min_treshold, max_treshold, image_threshed)
    return image_threshed

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


def hsv_image(image):
    hsv = cv.CreateImage(cv.GetSize(image), image.depth, 3)
    cv.CvtColor(image, hsv, cv.CV_BGR2HSV)
    return hsv


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
        
        
def sectorPos(kjsafjd):
    sectorpos = 0
    pi = 3.142
    slope = math.atan(((kjsafjd[0] - int(center)) / (kjsafjd[1] - int(center))))
    slope = slope - tilt*pi/180
#    print slope
    

    if (slope < pi / 3 and slope > 0):
        sectorpos = 4
    elif (slope < 2 * pi / 3):
        sectorpos = 3
    elif (slope < pi):
        sectorpos = 2
    elif (slope < 4 * pi / 3):
        sectorpos = 1
    elif (slope < 5 * pi / 3):
        sectorpos = 0
    elif (slope < 6 * pi / 3):
        sectorpos = 5
    return sectorpos

current_contour = cv.FindContours(cv.CloneImage(imageTreshold), cv.CreateMemStorage(), cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)

object_position = (0, 0)
if len(current_contour) != 0:
    object_position = contourCenter(largestContour(current_contour))
    

sectorpos = 0

slope = math.atan(((object_position[0] - int(center)) / (object_position[1] - int(center))))
slope = slope - tilt*pi/180;
print slope
pi = 3.142

if (slope < pi / 3 and slope > 0):
    sectorpos = 4
elif (slope < 2 * pi / 3):
    sectorpos = 3
elif (slope < pi):
    sectorpos = 2
elif (slope < 4 * pi / 3):
    sectorpos = 1
elif (slope < 5 * pi / 3):
    sectorpos = 0
elif (slope < 6 * pi / 3):
    sectorpos = 5
f = open('finalEquation.txt', 'r')
data = f.read()
data = data.split('\n')
for i in range(len(data)):
    data[i] = data[i].split(' ')
    if data[i] == ['']:
        data.pop(i)


data = zip(*data)
print data
directionToTake = [0, 0, 0] 

for i in range(6):
    if data[0][i] == '1':
        directionToTake[0] = i
    if data[1][i] == '1':
        directionToTake[1] = i
    if data[2][i] == '1':
        directionToTake[2] = i
print directionToTake, "direction to take"
ttt = directionToTake

answer = [0, 0, 0]
for i in range(3):
    directionToTake[i] = directionToTake[i] - sectorpos;
answer[0] = directionToTake[0]
sectorpos = answer[0]
for i in range(1, 3):
    directionToTake[i] = directionToTake[i] - sectorpos;
answer[1] = directionToTake[1]
sectorpos = answer[1]
for i in range(2, 3):
    directionToTake[i] = directionToTake[i] - sectorpos;
answer[2] = directionToTake[2]
print answer



f = open('radius.txt','r')
radius = f.read()
radius = int(radius)
radius = radius - int(center)
radiusdiff = radius/3

ser = serial.Serial('/dev/ttyUSB' + str(PORT), 9600)
#for sss in range(3):
#    if answer[i] < 0:
#        ser.write('left')
#    else:
#        ser.write('right')
#        while getBotCoord()[0]:
#            x = getBotCoord()
#            if 
#            if ((x[0][1]**2 + x[0][0]**2)**.5>radius):
#                ser.write('right')
#            else :
#                ser.write("straight")      
#            if se[0]
#        



    
while 1:
    coord = getBotCoord()[0]
    if ((x[0][1]**2 + x[0][0]**2)**.5>radius):
        ser.write('3')        #turn right
    else:
        ser.write('2')         #straight
    if sectorPos(coord) == ttt[i]:
        for sfdashf in range(40):
            ser.write('4')      #rotate right
        for sfdashf in range(40):
            ser.write('2')        
        for sfdashf in range(40):
            ser.write('0')      #rotate left
        radius = radius  - radiusdiff
        i = i+1
#    os.sleep(5)
    



 

    
    
    
    
