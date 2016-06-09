import cv2
import numpy as np 
cap=cv2.VideoCapture(0)
ret,first=cap.read()
l=float(1.0)

fgbg = cv2.BackgroundSubtractorMOG()

while True:
	back=first.copy()
	l=l+1
	ret1,frame=cap.read()
	if(l%5==0):
		back=cv2.addWeighted(back,0.4,frame,0.6,0)
	diff=cv2.absdiff(back,frame)
	#cv2.imshow('diff',diff)

	diff2=cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
	ret2,diff2thresh=cv2.threshold(diff2,5,255,cv2.THRESH_BINARY)
	
	ret3,diff3=cv2.threshold(diff2,15,255,cv2.THRESH_BINARY)
	blur1 = cv2.GaussianBlur(diff3,(5,5),0)
	kernel1 = np.ones((5,5),np.float32)/25
	diff4 = cv2.filter2D(blur1,-1,kernel1)
	kernel=np.ones((5,5),np.float32)/25
	
	#kernel2 = np.ones((5,5),np.uint8)
	erosion1 = cv2.erode(diff2,kernel1,iterations = 2)
	#erosion2 = cv2.erode(diff2thresh,kernel2,iterations = 1)

	opening=cv2.morphologyEx(diff4,cv2.MORPH_OPEN,kernel)
	#closing=cv2.morphologyEx(diff4,cv2.MORPH_CLOSE,kernel)

	#cv2.imshow('closing',closing)
	#cv2.imshow('opening',opening)

	#fgmask = fgbg.apply(diff2thresh) 
	#cv2.imshow('backgroundsubtractor',fgmask)
	
	#blur2 = cv2.GaussianBlur(diff2thresh,(5,5),0)
	#kernel = np.ones((5,5),np.float32)/25
	#diff5 = cv2.filter2D(blur2,-1,kernel)
	#ret4,diff5thresh=cv2.threshold(diff5,10,255,cv2.THRESH_BINARY)
	median = cv2.medianBlur(diff2thresh,5)
	ret4,erosionThresh=cv2.threshold(erosion1,30,255,cv2.THRESH_BINARY)
	
	
	contours,hierarchy = cv2.findContours(opening, 1, 2)
	cnt = contours[2]     
  	M = cv2.moments(cnt)
	print M
	
	#cv2.drawContours(erosion1, contours, -1, (0,255,0), 3)
	#contours,hierarchy = cv2.findContours(erosion1,2,1)
    	#print contours
    	#cnt = contours[4]

   	#hull = cv2.convexHull(cnt,returnPoints = False)
   	#defects = cv2.convexityDefects(cnt,hull)
 	#print defects
 	#if defects!=none:
   	#for i in range(defects.shape[0]):
   	#	s,e,f,d = defects[i,0]
    	#start = tuple(cnt[s][0])
    	#end = tuple(cnt[e][0])
    	#far = tuple(cnt[f][0])
    	#cv2.line(erosion1,start,end,[0,255,0],2)
    	#cv2.circle(erosion1,far,5,[0,0,255],-1)

	
	
	#cx = int(M['m10']/M['m00'])
	#cy = int(M['m01']/M['m00'])
	#hull = cv2.convexHull(cnt)
	#(x,y),radius = cv2.minEnclosingCircle(cnt)
	#center = (int(x),int(y))
	#radius = int(radius)
	#cv2.circle(diff2thresh,center,radius,(0,255,0),2)
	
	
	#erosion2, diff5, blur2,opening,closing not of any use.
	#Best is diif2 now. Concentrate on applying filters to it.
	#cv2.imshow('diff5',diff5)
	#cv2.imshow('blur2',blur2)
	#cv2.imshow('erosion2',erosion2)
	cv2.imshow('erosion1',erosion1)
	#cv2.imshow('median',median)	
	#cv2.imshow('diff5thresh',diff5thresh)
	#cv2.imshow('diff2thresh',diff2thresh)	
	#cv2.imshow('diff4',diff4)
	cv2.imshow('erosionthresh',erosionThresh)
	#cv2.imshow('diff2',diff2)
	#cv2.imshow('back',back)
	#cv2.imshow('diff3',diff3)
	#cv2.imshow('frame',frame)
	k=cv2.waitKey(30) & 0xff
	if k==27:
		break
cap.release()
cv2.destroyAllWindows()
print l
