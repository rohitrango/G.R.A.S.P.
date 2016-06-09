import cv2
import numpy as np 
import time
cap=cv2.VideoCapture(0)
l=float(1.0)
while l<100:
	ret,first=cap.read()
	l=l+1
back=first.copy()
while True:
	l=l+1
	ret,frame=cap.read()
	diff=cv2.absdiff(back,frame)
	#cv2.imshow('diff',diff)

	diff2=cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
	diff2=cv2.GaussianBlur(diff2,(5,5),0)
	ret,diff3=cv2.threshold(diff2,20,255,cv2.THRESH_BINARY)
	if(l%20==0 and l>100000):
		msk=diff3.copy()
		ret,msk2=cv2.threshold(msk,100,255,cv2.THRESH_BINARY_INV)
		a=cv2.bitwise_and(frame,frame,mask=msk2)
		b=cv2.bitwise_and(back,back,mask=msk)
		cv2.imshow('a',msk)
		cv2.imshow('b',msk2)
		back=cv2.addWeighted(back,0.8,a,0.2,0)
		back=cv2.addWeighted(back,0.8,b,0.2,0)
		#back=cv2.addWeighted(back,0.9,frame,0.1,0)
		print "hello"
	cv2.imshow('diff2',diff2)
	cv2.imshow('back',back)
	cv2.imshow('diff3',diff3)
	#cv2.imshow('frame',frame)
	k=cv2.waitKey(30) & 0xff
	if k==27:
		break
cap.release()
cv2.destroyAllWindows()
print l
