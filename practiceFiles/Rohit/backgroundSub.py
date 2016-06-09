import cv2
import numpy as np

cam = cv2.VideoCapture(0)
fgbg = cv2.BackgroundSubtractorMOG2()

while(1):
	ret, frame = cam.read()
	fgmask = fgbg.apply(frame)
	cv2.imshow('frame', fgmask)
	k = cv2.waitKey(1) and 0xFF
	if k==27:
		break

cam.release()
cv2.destroyAllWindows()