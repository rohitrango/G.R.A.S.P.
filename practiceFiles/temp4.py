import cv2
import numpy as np 
cap=cv2.VideoCapture(0)
l=1
while l<10:
	ret,frame=cap.read()
	l=l+1
back=frame.copy()
mask=np.zeros((480,640),dtype=np.uint8)
while True:
	l=l+1
	ret,frame=cap.read()
	diff=cv2.absdiff(back,frame)
	diff=cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
	diffsq=np.power(diff,2)
	ret,mask1=cv2.threshold(diffsq,200,255,cv2.THRESH_BINARY)
	cv2.imshow('diff',diffsq)
	sum_vec=np.sum(diffsq,axis=0)
	mask[diffsq>230]=255
	cv2.imshow('mask',mask1)
	cv2.imshow('diff',diff)
	k=cv2.waitKey(30) & 0xff
	if k==27:
		break
print back2.shape
cap.release()
cv2.destroyAllWindows()