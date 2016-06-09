import cv2
import numpy as np 
from time import sleep

def hsvConvert(rgb):
	rgb = np.uint8([[rgb]])
	hsv = cv2.cvtColor(rgb,cv2.COLOR_BGR2HSV)
	hsvColors.append(hsv)

cam = cv2.VideoCapture(0)

points = [{"x":100,"y":100},{"x":120, "y":120}, {"x":110 , "y":230}]
rectDim = {"width":10,"height":15}
green = (0,255,0)
font = cv2.FONT_HERSHEY_SIMPLEX	
colorProfile = []								# get color profile of skin
hsvColors = []

i = 0
while i<50:										# give time to place his hand

	ret, frame = cam.read()
	frame = cv2.flip(frame,90)
	for point in points:
		f = frame[point["x"]+rectDim["width"]/2,point["y"] + rectDim["height"]/2]
		textString = str(f[0]) + " " + str(f[1])+" " + str(f[2])
		cv2.putText(frame,textString, (point["x"],point["y"]), font, 0.5, (0,255,0),2)
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

for k in colorProfile:
	hsvConvert(k)
# print hsvColors

cv2.destroyAllWindows()


while(True):
	ret, frame = cam.read()
	frame = cv2.flip(frame,90)
	pyrFrame = cv2.pyrDown(frame)
	pyrFrame = cv2.resize(pyrFrame,None,fx=2, fy=2, interpolation = cv2.INTER_CUBIC)
	blurred = cv2.blur(pyrFrame,(5,5))

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
		lowerCol = np.array([h-10,50,50])
		upperCol = np.array([h+10,255,255])
		mask = cv2.inRange(myBlur,lowerCol,upperCol)
		res = cv2.bitwise_and(blurred,blurred,mask=mask)
		cv2.imshow(str(temp),res)
		temp+=1


	cv2.imshow('blurred', blurred)
	cv2.imshow("pyrFrame",pyrFrame)
	cv2.imshow('frame',frame)

	k = cv2.waitKey(1)
	if k==ord('q'):
		break

cam.release()
cv2.destroyAllWindows()