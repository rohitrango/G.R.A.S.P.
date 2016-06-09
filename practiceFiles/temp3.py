import cv2
import numpy as np 
import time
cap=cv2.VideoCapture(0)
subtractor=cv2.BackgroundSubtractorMOG()
l=float(1.0)
while l<15:
	ret,first=cap.read()
	l=l+1
back=first.copy()
back2=cv2.cvtColor(back,cv2.COLOR_BGR2HSV)

while True:
	l=l+1
	ret,frame=cap.read()
	hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	diff=cv2.absdiff(back2,frame)
	driff=cv2.cvtColor(diff,cv2.COLOR_HSV2BGR)
	cv2.imshow('driff',driff)
	driff2=cv2.cvtColor(driff,cv2.COLOR_BGR2GRAY)
	cv2.imshow('driff2',driff2)
	ret,msk=cv2.threshold(driff2,60,255,cv2.THRESH_BINARY)
	cv2.imshow('msk',msk)

	#th = cv2.adaptiveThreshold(driff2, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,501,0)
	#cv2.imshow('th',th)



	#lower_red=np.array([100,50,50])
	#upper_red=np.array([255,255,255])
	#mask=cv2.inRange(hsv,lower_red,upper_red)
	#res=cv2.bitwise_and(diff,diff,mask=mask)
	#cv2.imshow('res',res)
	ifc v2.waitKey(1) & 0xff==ord('q'):
		break
cap.release()
cv2.destroyAllWindows()