import cv2
import numpy as np 

cam = cv2.VideoCapture(0)
prevFrame, nextFrame = [], []

while True:
	ret, frame = cam.read()
	frame = cv2.flip(frame,90)
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	fgbg = cv2.BackgroundSubtractorMOG2()
	if(prevFrame==[] and nextFrame==[]):
		prevFrame = frame.copy()
	elif prevFrame!=[] and nextFrame==[]:
		nextFrame = frame.copy()
	else:
		prevFrame = nextFrame.copy()
		nextFrame = frame.copy()
		currentFrame=nextFrame-prevFrame
		cv2.imshow("frame",currentFrame)
		fgmask = fgbg.apply(currentFrame)
		kernel = np.ones((5,5),np.uint8)
		eroded = cv2.erode(fgmask,kernel,iterations=1)
		
		fgmask = cv2.medianBlur(eroded,5)
		ret, final = cv2.threshold(fgmask,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
		cv2.imshow("threshold",final)
		cv2.imshow("eroded",eroded)
		cv2.imshow("fgmask",fgmask)
		

	k = cv2.waitKey(10) & 0xff
	if k==ord('q'):
		break

cam.release()
cv2.destroyAllWindows()

