import numpy as numpy
import cv2

cam = cv2.VideoCapture(0)
print "\n\nPress 'q' to exit.\n\n"
while True:
	ret,frame = cam.read()
	frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	cv2.imshow('Test Script',frame)
	if(cv2.waitKey(1) & 0xFF == ord('q')):
		break

cam.release()
cv2.destroyAllWindows()
print "Cam released and all windows terminated."