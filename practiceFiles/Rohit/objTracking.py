import cv2, numpy as np
cam = cv2.VideoCapture(0)
while(1):
	ret, frame = cam.read()
	frame = cv2.flip(frame,90)
	hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	lowerPink = np.array([120,50,50])				### HSV value
	upperPink = np.array([150,255,255])				### HSV value

	mask = cv2.inRange(hsv,lowerPink,upperPink)
	res = cv2.bitwise_and(frame, frame, mask=mask)	### mask
	cv2.imshow('Frame', frame)
	cv2.imshow('Mask', mask)
	cv2.imshow('res', res)
	if(cv2.waitKey(1) & 0xFF == ord('q')):
		break

cam.release()
cv2.destroyAllWindows()

# use the helper script rgb2hsv.py to get hsv values