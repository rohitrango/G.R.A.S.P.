import cv2, numpy as np
from matplotlib import pyplot as plt

cam = cv2.VideoCapture(0)
print "Press 'q' to exit."
while True:
	ret, frame = cam.read()
	frame = cv2.flip(frame,90)
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	ret, thresh = cv2.threshold(gray,128,255,cv2.THRESH_BINARY)
	adaptive = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
	gaussian = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
	cv2.imshow('Original', frame)
	cv2.imshow('Adaptive threshold', adaptive)
	cv2.imshow('Threshold',thresh)
	cv2.imshow('Adaptive Gaussian threshold', gaussian)
	if(cv2.waitKey(1) & 0xFF==ord('q')):
		break

cam.release()
cv2.destroyAllWindows()