import cv2, numpy as np 
import math

cam = cv2.VideoCapture(0)
fgbg = cv2.BackgroundSubtractorMOG2()
green = (0,255,0)
blue = (255,0,0)
red = (0,0,255)

def P2P(a,b):
	return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def angle(a,b,c):
	return math.fabs(math.atan2(a[1]-b[1], a[0]-b[0]) - math.atan2(c[1]-b[1],c[0]-b[0]) ) 

while(True):
	ret, frame = cam.read()
	frame = cv2.flip(frame,90)
	finalColor = frame.copy()
	frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	fgmask = fgbg.apply(frame)

	kernel = np.ones((5,5),np.uint8)
	eroded = cv2.erode(fgmask,kernel,iterations=1)

	fgmask = cv2.medianBlur(eroded,7)
	ret, final = cv2.threshold(fgmask,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

	contours, hierarchy = cv2.findContours(final.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
	biggestC = None
	for c in contours:
		if(biggestC==None):
			biggestC = c
		else:
			if cv2.contourArea(c) > cv2.contourArea(biggestC):
				biggestC = c

	if biggestC!=None:
		
		x,y,w,h = cv2.boundingRect(biggestC)
		cv2.rectangle(finalColor,(x,y),(x+w,y+h),blue,2)
		
		hull = cv2.convexHull(biggestC, returnPoints=False)
		approx = cv2.approxPolyDP(biggestC,18,True)
		defects = cv2.convexityDefects(biggestC,hull)
		newdefects = []
		
		if(defects!=None):
			for i in range(defects.shape[0]):
				s,e,f,d = defects[i,0]
				start = tuple(biggestC[s][0])
				end = tuple(biggestC[e][0])
				far = tuple(biggestC[f][0])
				if (min(P2P(start,far),P2P(end,far)) >= 0.1*h) and (angle(start,far,end)<=80.0*math.pi/180):
					newdefects.append([start,end,far])
				else:
					newdefects.append([start,end,-1])

		if(newdefects!=[]):

			for i in newdefects:
				start = i[0]
				end = i[1]
				far = i[2]
				cv2.line(finalColor,start,end,green,2)
				if(far!=-1):
					cv2.circle(finalColor,start,5,blue,-1)
					cv2.circle(finalColor,far,5,red,-1)
		
	# cv2.drawContours(finalColor,[biggestC],-1,green,2)

	cv2.imshow('finalColor', finalColor)
	cv2.imshow('fgmask',fgmask)
	cv2.imshow('eroded', eroded)
	cv2.imshow('final', final)

	k = cv2.waitKey(1)
	if k==ord('q'):
		break

cam.release()
cv2.destroyAllWindows()