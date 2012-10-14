import cv

class hsvVals_MouseClick:
    def on_mouse(self,event, x, y, flag, param):
        if(event == cv.CV_EVENT_LBUTTONDOWN):
            self.x_co = x
            self.y_co = y
    def getHsvRange(self):
        self.x_co = 0
        self.y_co = 0
    
        cv.NamedWindow('camera feed', cv.CV_WINDOW_AUTOSIZE)
        capture = cv.CaptureFromCAM(1)
        
        
        font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 0.5, 1, 0, 2, 8)
        
        
        while True:
            src = cv.QueryFrame(capture)
#            src = cv.LoadImage('2012_automata.jpg')
            cv.Smooth(src, src, cv.CV_BLUR, 3)
            hsv = cv.CreateImage(cv.GetSize(src), src.depth, 3)
            cv.CvtColor(src, hsv, cv.CV_BGR2HSV)
            cv.SetMouseCallback("camera feed", self.on_mouse, 0);
            s = cv.Get2D(hsv, self.y_co, self.x_co)
    #        print "H:", s[0], "      S:", s[1], "       V:", s[2]
            cv.PutText(src, str(s[0]) + "," + str(s[1]) + "," + str(s[2]), (self.x_co, self.y_co), font, (55, 25, 255))
            cv.ShowImage("camera feed", src)
            if cv.WaitKey(10) == 27:
                return (s[0],s[1],s[2])
                break