import cv2
import numpy as np 

cam = cv2.VideoCapture(0)
# fgbg = cv2.BackgroundSubtractorMOG2()
prevFrame, nextFrame = [], []

while True:
	ret, frame = cam.read()
	frame = cv2.flip(frame,90)
	# frame = fgbg.apply(frame)
	kernel = np.ones((5,5),np.uint8)
	# frame = cv2.medianBlur(frame,7)
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	if(prevFrame==[] and nextFrame==[]):
		prevFrame = frame.copy()
	elif prevFrame!=[] and nextFrame==[]:
		nextFrame = frame.copy()
	else:
		prevFrame = nextFrame
		nextFrame = frame
		final = cv2.absdiff(prevFrame,nextFrame)
		final = cv2.medianBlur(final,5)
		# final = cv2.erode(final,kernel,iterations=1)
		cv2.imshow("frame",final)
		# cv2.imshow('sub',fgmask)

	k = cv2.waitKey(10)
	if k==ord('q'):
		break

cam.release()
cv2.destroyAllWindows()

