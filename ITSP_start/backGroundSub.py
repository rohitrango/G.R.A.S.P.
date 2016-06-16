import cv2, numpy as np 
import math
from functions import *
import gestures

cam = cv2.VideoCapture(0)
fgbg = cv2.BackgroundSubtractorMOG2()

while(True):
	ret, frame = cam.read()
	frame = cv2.flip(frame,90)
	finalColor = frame.copy()
	frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	fgmask = fgbg.apply(frame)

	kernel = np.ones((5,5),np.uint8)
	eroded = cv2.erode(fgmask,kernel,iterations=1)

	fgmask = cv2.medianBlur(eroded,7)
	ret, final = cv2.threshold(fgmask,0,255,cv2.THRESH_BINARY)		#+cv2.THRESH_OTSU
	
	if np.sum(final>150) > np.sum(final<150):		# negating the colors in case of problems
		final = 255-final



	contours, hierarchy = cv2.findContours(final.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
	
	if(contours!=[]):
		biggestC = max(contours, key=cv2.contourArea)
	else:
		biggestC=None


	if biggestC!=None:
		#------------------------------------
		# for i in contours:
		# 	if cv2.contourArea(i)!=cv2.contourArea(biggestC):
		# 		cv2.drawContours(final,[i],0,(0,0,0),-1)

		M = cv2.moments(biggestC)
		center = None
		if(M['m00']):
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
			cv2.circle(finalColor,center,10,yellow,2)

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
				if (min(P2P(start,far),P2P(end,far)) >= 0.1*h) and (angle(start,far,end)<=80.0*math.pi/180 and far[1]<=int(y+h/2)):
					newdefects.append([start,end,far])
				else:
					newdefects.append([start,end,-1])

		if(newdefects!=[]):
			xcenter,ycenter = 0,0
			centerCount=0
			
			for i in newdefects:
				start = i[0]
				end = i[1]
				far = i[2]
				cv2.line(finalColor,start,end,(0,255,0),2)
				if(far!=-1):
					xcenter+=far[0]			#finding center of x,y
					ycenter+=far[1]
					centerCount+=1
					cv2.circle(finalColor,start,5,blue,-1)
					cv2.circle(finalColor,far,5,red,-1)

			if(centerCount>0):				# we have a point to track

				# draw the circle
				xcenter/=centerCount
				ycenter/=centerCount
				# cv2.circle(finalColor,(xcenter,ycenter),10,yellow,2)

				if(gestures.prevPoint==None and gestures.nextPoint==None):	# start
					gestures.prevPoint = (xcenter,ycenter)
				elif (gestures.nextPoint == None):							# 1st iteration
					gestures.nextPoint = (xcenter,ycenter)
				else:
					gestures.prevPoint = gestures.nextPoint
					gestures.nextPoint = (xcenter,ycenter)
				gestures.recordGesture()




		
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