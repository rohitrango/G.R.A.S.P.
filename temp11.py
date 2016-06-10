import cv2
import numpy as np


cap = cv2.VideoCapture(0)

def nothing(x):
    pass
# Creating a window for later use
cv2.namedWindow('result')

# Starting with 100's to prevent error while masking
h,s,v = 100,100,100

# Creating track bar
cv2.createTrackbar('h', 'result',0,179,nothing)
cv2.createTrackbar('s', 'result',0,255,nothing)
cv2.createTrackbar('v', 'result',0,255,nothing)

while(1):

    _, frame = cap.read()

    #converting to HSV
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    # get info from track bar and appy to result
    h = cv2.getTrackbarPos('h','result')
    s = cv2.getTrackbarPos('s','result')
    v = cv2.getTrackbarPos('v','result')

    # Normal masking algorithm
    lower_blue = np.array([h,s,v])
    upper_blue = np.array([255,255,255])

    mask = cv2.inRange(hsv,lower_blue, upper_blue)

    result = cv2.bitwise_and(frame,frame,mask = mask)
    
    blur = cv2.GaussianBlur(result,(5,5),0)
    kernel=np.ones((5,5),np.float32)/25
    #erosion = cv2.erode(blur,kernel,iterations = 1)
    dilation = cv2.dilate(blur, kernel, iterations=1)

    mask3 = cv2.Canny(dilation,100,200)
    copymask3 = mask3.copy()
    contours, hierarchy = cv2.findContours(copymask3, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # we have the contours, time for the biggest one
    biggestCountour = None
    for c in contours:
        if biggestCountour == None:
            biggestCountour = c
        else:
            # if(cv2.contourArea(c)>cv2.contourArea(biggestCountour)):
            if(cv2.arcLength(c,True)>cv2.arcLength(biggestCountour,True)):
                biggestCountour = c
    # we found the biggest contour, time to find convexity defects
    #hull = cv2.convexHull(biggestCountour)

    cv2.drawContours(dilation,[biggestCountour],-1,(0,255,0),3)


    cv2.imshow('result',result)
    #cv2.imshow('erosion',erosion)
    cv2.imshow('dilation',dilation)
    #cv2.imshow('hull',hull)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()

cv2.destroyAllWindows()