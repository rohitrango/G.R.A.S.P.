import cv2
import numpy as np
from time import sleep

def hsvConvert(rgb):
	rgb = np.uint8([[rgb]])
	hsv = cv2.cvtColor(rgb,cv2.COLOR_BGR2HSV)
	hsvColors.append(hsv)

cam = cv2.VideoCapture(0)

points = [{"x":300,"y":100},{"x":280, "y":120}, {"x":310 , "y":90},{"x":300,"y":130},{"x":290, "y":150}]
rectDim = {"width":10,"height":15}
green = (0,255,0)
red = (0,0,255)
blue = (255,0,0)
font = cv2.FONT_HERSHEY_SIMPLEX
colorProfile = []								# get color profile of skin
hsvColors = []
#<<<<
mask2=np.zeros((480,680),dtype=np.uint8)
#>>>>
i = 0
while i<50:										# give time to place his hand

	ret, frame = cam.read()
	frame = cv2.flip(frame,90)
	for point in points:
		f = frame[point["x"]+rectDim["width"]/2,point["y"] + rectDim["height"]/2]
		textString = str(f[0]) + " " + str(f[1])+" " + str(f[2])
		# cv2.putText(frame,textString, (point["x"],point["y"]), font, 0.5, (0,255,0),2)
		cv2.rectangle(frame,(point["x"],point["y"]),(point["x"]+rectDim["width"],point["y"]+rectDim["height"]),green,2)
	cv2.imshow('Place your palm within the ROI',frame)

	k = cv2.waitKey(1)
	if k==ord('q'):
		i = 49

	if i==49:
		for point in points:
			nthColor = frame[point["x"]+rectDim["width"]/2,point["y"] + rectDim["height"]/2]
			colorProfile.append(nthColor)
		print colorProfile

	i+=1

#<<<
#pyrFrame = cv2.pyrDown(frame)
#pyrFrame = cv2.resize(pyrFrame,None,fx=2, fy=2, interpolation = cv2.INTER_CUBIC)
#back = cv2.blur(pyrFrame,(5,5))
back=frame.copy()
#>>>>

for k in colorProfile:
	hsvConvert(k)
# print hsvColors

cv2.destroyAllWindows()

duration=4
while(True):
	ret, frame = cam.read()
	# frame = frame[240:480,0:320]				# as of now, we work on only few parts
	frame = cv2.flip(frame,90)
	pyrFrame = cv2.pyrDown(frame)
	pyrFrame = cv2.resize(pyrFrame,None,fx=2, fy=2, interpolation = cv2.INTER_CUBIC)
	blurred = cv2.blur(pyrFrame,(5,5))

	#<<<<
	# mask2=np.zeros((480,680),dtype=np.uint8)
	# i=i+1
	# if(i%5==0):
	# 	back=cv2.addWeighted(back,0.9,frame,0.1,0)
	# diff=cv2.absdiff(back,frame)
	# diff=cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
	# diffsq=np.power(diff,2)
	# mask2[diffsq>150]=255
	# cv2.imshow('mask2',mask2)
	#>>>>

	# hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	# lowerPink = np.array([120,50,50])				### HSV value
	# upperPink = np.array([150,255,255])				### HSV value

	# mask = cv2.inRange(hsv,lowerPink,upperPink)
	# res = cv2.bitwise_and(frame, frame, mask=mask)	### mask
	# cv2.imshow('Frame', frame)
	# cv2.imshow('Mask', mask)
	# cv2.imshow('res', res)

	temp = 0
	for hsvColor in hsvColors:
		myBlur = cv2.cvtColor(blurred,cv2.COLOR_BGR2HSV)
		h = hsvColor[0][0][0]
		lowerCol = np.array([h-7,45,45])
		upperCol = np.array([h+8,255,255])
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
		cv2.imshow(str(temp),res)
		temp+=1
	finalmask=mask3.copy()
	mask4 = cv2.medianBlur(mask3,7)
	mask3 = cv2.medianBlur(mask3,5)
	mask3 = cv2.Canny(mask3,100,200)
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
	if(biggestCountour!=None):
		hull = cv2.convexHull(biggestCountour, returnPoints=False)
		approx = cv2.approxPolyDP(biggestCountour,18,True)
		defects = cv2.convexityDefects(biggestCountour,hull)
		# we have the defects, time to remove redundant ones

		# removed redundant defects (not yet :P)
		# print defects.shape

		if(defects!=None):
			for i in range(defects.shape[0]):
			    s,e,f,d = defects[i,0]
			    start = tuple(biggestCountour[s][0])
			    end = tuple(biggestCountour[e][0])
			    far = tuple(biggestCountour[f][0])
			    cv2.line(frame,start,end,green,2)
			    cv2.circle(frame,start,5,blue,-1)
			    cv2.circle(frame,far,5,red,-1)


		# epsilon = 0.1*cv2.arcLength(biggestCountour,True)

		x,y,w,h = cv2.boundingRect(biggestCountour)
		cv2.rectangle(frame,(x,y),(x+w,y+h),blue,2)
		
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
	cv2.imshow('copymask3' , copymask3)
	cv2.imshow('mask4', mask4)
	cv2.imshow('blurred', blurred)
	cv2.imshow("pyrFrame",pyrFrame)
	cv2.imshow('frame',frame)
	cv2.imshow('mask3',mask3)
	cv2.imshow('finalmask',finalmask)
	k = cv2.waitKey(1) & 0xff
	if k==ord('q'):
		break
	i+=1
	if(i%duration==0):
		pts=[mask3!=0]


print pts
cam.release()
cv2.destroyAllWindows()
