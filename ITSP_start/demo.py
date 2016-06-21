import cv2
import numpy as np
from time import sleep
from functions import *
import math
import gestures

def hsvConvert(rgb):
	rgb = np.uint8([[rgb]])
	hsv = cv2.cvtColor(rgb,cv2.COLOR_BGR2HSV)
	hsvColors.append(hsv)

# gestures.init()

cam = cv2.VideoCapture(0)
newdefects = []
points = [					#240*320
	{"x":120,"y":90},
	{"x":80, "y":140}, 
	{"x":160 , "y":140},
	{"x":100,"y":210},
	{"x":150, "y":210},
	{"x":120, "y":160}]

rectDim = {"width":10,"height":15}
green = (0,255,0)
red = (0,0,255)
blue = (255,0,0)
font = cv2.FONT_HERSHEY_SIMPLEX
# colorProfile = []								# get color profile of skin
hsvColors = []
cnscDef = 0										# no of consecutive no-defects

mask2=np.zeros((480,680),dtype=np.uint8)

i = 0
N=100
while i<N:										# give time to place his hand

	ret, frame = cam.read()
	frame = frame[240:480,0:320]
	frame = cv2.flip(frame,90)
	for point in points:
		f = frame[point["x"]+rectDim["width"]/2,point["y"] + rectDim["height"]/2]
		textString = str(f[0]) + " " + str(f[1])+" " + str(f[2])
		cv2.putText(frame,"Put your hand in the green boxes",(10,20),font,0.5,green,2)
		# cv2.putText(frame,textString, (point["x"],point["y"]), font, 0.5, (0,255,0),2)
		cv2.rectangle(frame,(point["x"],point["y"]),(point["x"]+rectDim["width"],point["y"]+rectDim["height"]),green,2)
	
	cv2.imshow('Place your palm in the green boxes',frame)

	k = cv2.waitKey(1)
	if k==ord('q'):
		i = N-1

	if i==N-1:
		for point in points:
			roi = frame[point["x"]:point["x"]+rectDim["width"] , point["y"]:point["y"]+rectDim["height"]] 
			roi = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
			hVal = roi[0:rectDim["width"], 0:rectDim["height"], 0]
			sVal = roi[0:rectDim["width"], 0:rectDim["height"], 1]
			vVal = roi[0:rectDim["width"], 0:rectDim["height"], 2]

			h,s,v = np.median(hVal), np.median(sVal), np.median(vVal)
			hsvColors.append([h,s,v])
	i+=1

back=frame.copy()
cv2.destroyAllWindows()
print "Entering Idle Mode. Press 't' for track mode, 'i' for idle mode, 'q' to quit."

while(True):
	ret, frame = cam.read()
	frame = cv2.flip(frame,90)
	pyrFrame = cv2.pyrDown(frame)
	pyrFrame = cv2.resize(pyrFrame,None,fx=2, fy=2, interpolation = cv2.INTER_CUBIC)
	blurred = cv2.blur(pyrFrame,(5,5))

	temp = 0
	for hsvColor in hsvColors:
		myBlur = cv2.cvtColor(blurred,cv2.COLOR_BGR2HSV)
		# h = hsvColor[0][0][0]
		h = hsvColor[0]
		lowerCol = np.array([max(3.0,h-10),100,100])
		upperCol = np.array([h+10,255,255])
		mask = cv2.inRange(myBlur,lowerCol,upperCol)
		res = cv2.bitwise_and(blurred,blurred,mask=mask)
		res = cv2.cvtColor(res,cv2.COLOR_HSV2BGR)
		res = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
		_, res = cv2.threshold(res,20,255,cv2.THRESH_BINARY)
		if(temp==0):
			mask3=res.copy()
		else:
			pts=[mask3==0]
			mask3[pts]=res[pts]
		# cv2.imshow(str(temp),res)
		temp+=1

	##########################################################################################
	lSkin = np.array([5,38,51])
	uSkin = np.array([17,250,242])
	hsvFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	hsvFrame = cv2.GaussianBlur(hsvFrame,(7,7),1,1)
	skinMask = cv2.inRange(hsvFrame,lSkin,uSkin)
	skinMasked = cv2.bitwise_and(hsvFrame,hsvFrame,mask=skinMask)
	skinMasked = cv2.cvtColor(skinMasked,cv2.COLOR_HSV2BGR)
	skinMasked = cv2.cvtColor(skinMasked,cv2.COLOR_BGR2GRAY)
	_,skinMasked = cv2.threshold(skinMasked,60,255,cv2.THRESH_BINARY)
	
	finalSkin = cv2.morphologyEx(skinMasked,cv2.MORPH_ERODE,np.ones((3,3),dtype=np.uint8),iterations=2)
	finalSkin = cv2.morphologyEx(finalSkin,cv2.MORPH_OPEN,np.ones((5,5), dtype=np.uint8),iterations=1)
	finalSkin = cv2.morphologyEx(finalSkin,cv2.MORPH_CLOSE,np.ones((9,9),dtype=np.uint8),iterations=1)
	finalSkin = cv2.medianBlur(finalSkin,11)
	cv2.imshow('skinMasked',skinMasked)
	cv2.imshow('finalSkin', finalSkin)
	#########################################################################################

	mask4 = cv2.medianBlur(mask3,7)
	mask3 = cv2.medianBlur(mask3,5)
	erodeMask = mask3.copy()
	mask3 = cv2.Canny(mask3,100,200)
	copymask3 = mask3.copy()
	contours, hierarchy = cv2.findContours(copymask3, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	noOfDefects = 0
	# we have the contours, time for the biggest one
	biggestCountour = None
	for i in contours:
		if(biggestCountour==None):
			biggestCountour = i
		else:
			if(cv2.arcLength(biggestCountour,True) < cv2.arcLength(i,True)):
				biggestCountour = i

	# we found the biggest contour, time to find convexity defects
	if(biggestCountour!=None):
		try:
			hull = cv2.convexHull(biggestCountour, returnPoints=False)
		except:
			print "No Hull"
		approx = cv2.approxPolyDP(biggestCountour,18,True)
		defects = cv2.convexityDefects(biggestCountour,hull)

		x,y,w,h = cv2.boundingRect(biggestCountour)
		cv2.rectangle(frame,(x,y),(x+w,y+h),blue,2)

		# we need to find the moments
		M = cv2.moments(biggestCountour)

		cx = cy = None
		if(M['m00']!=0):
			cx = int(M['m10']/M['m00'])
			cy = int(M['m01']/M['m00'])
			# print cx,cy , "\n\n\n\n"
			cv2.circle(frame,(cx,cy),10,yellow,2)

			if(gestures.prevPoint==None and gestures.nextPoint==None):	# start
				gestures.prevPoint = (cx,cy)
			elif (gestures.nextPoint == None):							# 1st iteration
				gestures.nextPoint = (cx,cy)
			else:
				gestures.prevPoint = gestures.nextPoint
				gestures.nextPoint = (cx,cy)
				gestures.recordGesture()	

		# we have the defects, time to remove redundant ones
		newdefects = []

		if(defects!=None):
			for i in range(defects.shape[0]):
			    s,e,f,d = defects[i,0]
			    start = tuple(biggestCountour[s][0])
			    end = tuple(biggestCountour[e][0])
			    far = tuple(biggestCountour[f][0])
			    # cv2.line(frame,start,end,green,2)
			    # cv2.circle(frame,start,5,blue,-1)
			    # cv2.circle(frame,far,5,red,-1)

			    if (min(P2P(start,far),P2P(end,far)) >= 0.25*h) and (angle(start,far,end)<=80.0*math.pi/180):
			    	newdefects.append([start,end,far])
			    	noOfDefects+=1
			    else:
			    	newdefects.append([start,end,-1])

# we have found the biggest rectangle. and filtering of defects is done above as well.
# find the center of contours and track the point 

		if(newdefects!=[]):
			xcenter,ycenter = 0,0
			centerCount=0
			
			for i in newdefects:
				start = i[0]
				end = i[1]
				far = i[2]
				cv2.line(frame,start,end,(0,255,0),2)
				if(far!=-1):
					xcenter+=far[0]			#finding center of x,y
					ycenter+=far[1]
					centerCount+=1
					cv2.circle(frame,start,5,blue,-1)
					cv2.circle(frame,far,5,red,-1)


	# cv2.drawContours(frame,[biggestCountour],-1,green,3)
	# cv2.drawContours(frame,approx,-1,red,5)
	# cv2.drawContours(frame,hull,-1,blue,5)

	# M = cv2.moments(biggestCountour)
	# if(M['m00']):
	# 	cx = int(M['m10']/M['m00'])
	# 	cy = int(M['m01']/M['m00'])
	# else:
	# 	cx = cy = 0
	# cv2.circle(frame,(cx,cy),5,red,3)
	# print contours[0]
	anotherKernel = np.ones((9,9),np.uint8)
	erodeFinger = cv2.erode(erodeMask,anotherKernel,iterations=2)

	# cv2.imshow('erodeFinger',erodeFinger)
	cv2.imshow('copymask3' , copymask3)
	cv2.imshow('mask4', mask4)
	# cv2.imshow('blurred', blurred)
	# cv2.imshow("pyrFrame",pyrFrame)
	cv2.imshow('frame',frame)
	cv2.imshow('mask3',mask3)

	k = cv2.waitKey(1) & 0xff
	if k==ord('q'):
		print "Exiting program. Thanks for using!"
		break
	elif k==ord('t'):		# track mode
		gestures.changeGestureMode("track")
	elif k==ord('i'):		# idle mode
		gestures.changeGestureMode("idle")

cam.release()
cv2.destroyAllWindows()
