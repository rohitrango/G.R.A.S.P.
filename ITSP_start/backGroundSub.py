import cv2, numpy as np 
import math

cam = cv2.VideoCapture(0)
fgbg = cv2.BackgroundSubtractorMOG2()
green = (0,255,0)
blue = (255,0,0)
red = (0,0,255)

def P2P(a,b):
	return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def angle(a,b,c):
	return math.fabs(math.atan2(a[1]-b[1], a[0]-b[0]) - math.atan2(c[1]-b[1],c[0]-b[0]) ) 
motionhistory=[[0 for j in xrange(5)]for i in xrange(20)]
motion=np.zeros([10,4])
currindex=0
minindex=np.empty(500)
maxindex=np.empty(500)
lowerrow=-1
upperrow=-1
line1=-1
line2=-1
line3=-1
std1=10
std2=10
std3=10
std4=30
flag=-1
def findindex(row_no):
	global lowerrow,upperrow	

	for index,j in enumerate(final[row_no]):
		if(j>0):
#---------we can tak row_no + x as a variable to make it faster
			#print row_no+y
			#print minindex
			if(lowerrow==-1):
				lowerrow=row_no
			if(minindex[row_no+y]==-1):
				minindex[row_no+y]=index
				upperrow=row_no
			maxindex[row_no+y]=index
def combineindices():
	lowerrow=-1
	upperrow=-1
	minindex.fill(-1)
	maxindex.fill(-1)
	for row in range(0,h):
		findindex(row)
def combineindices2():
	global minindex,maxindex,w
	minindex.fill(-1)
	maxindex.fill(-1)
	minindex=np.argmax(canny,0)
	tempframe=cv2.flip(canny,90)
	maxindex=np.argmax(tempframe,0)
	maxindex=-1*maxindex+w+x
	minindex=minindex+x
def findlines():
	if (np.std(minindex)<std1):
		flag=1
		line1=np.mean(minindex)
		line2temp,line3temp=np.array_split(maxindex,2)
		line2=np.mean(line2temp)
		line3=np.mean(line3temp)
	else:
		flag=2
		line1=np.mean(maxindex)
		line2temp,line3temp=np.array_split(maxindex,2)
		line2=np.mean(line3temp)
		line3=np.mean(line2temp)
	temp=np.array([flag,line1,line2,line3])
	motion[currindex]=temp
	currindex+=1
	if(currindex==5):
		deviation=np.std(motion,0)
		#put a condition that if no motion, then reset it to 0
	if(currindex==18):
		if(motion[0][0]-motion[18][0]):
			deviation=np.std(motion,0)
			if(deviation[1]<std1):
				if(deviation[2]<std2):
					if(deviation[3]>std4):
						#gesture detected!


	print motion

while(True):
	ret, frame = cam.read()
	frame = cv2.flip(frame,90)
	finalColor = frame.copy()
	frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	fgmask = fgbg.apply(frame)

	kernel = np.ones((5,5),np.uint8)
	eroded = cv2.erode(fgmask,kernel,iterations=1)

	fgmask = cv2.medianBlur(eroded,7)
	ret, final = cv2.threshold(fgmask,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

	contours, hierarchy = cv2.findContours(final.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
	biggestC = None
	for c in contours:
		if(biggestC==None):
			biggestC = c
		else:
			if cv2.contourArea(c) > cv2.contourArea(biggestC):
				biggestC = c

	if biggestC!=None:
		
		x,y,w,h = cv2.boundingRect(biggestC)
		cv2.rectangle(finalColor,(x,y),(x+w,y+h),blue,2)
		hull = cv2.convexHull(biggestC, returnPoints=False)
		approx = cv2.approxPolyDP(biggestC,18,True)
		try:
			defects = cv2.convexityDefects(biggestCountour,hull)
		except:
			print "caught error!"
			print biggestContour
		newdefects = []
		
		if(defects!=None):
			for i in range(defects.shape[0]):
				s,e,f,d = defects[i,0]
				start = tuple(biggestC[s][0])
				end = tuple(biggestC[e][0])
				far = tuple(biggestC[f][0])
				if (min(P2P(start,far),P2P(end,far)) >= 0.1*h) and (angle(start,far,end)<=80.0*math.pi/180):
					newdefects.append([start,end,far])
				else:
					newdefects.append([start,end,-1])

		if(newdefects!=[]):
			#-----------------------------------------------------------------------
			roi=final[x:x+w,y:y+h]
			#pts=[roi==255]
			canny=cv2.Canny(roi,100,200)
			combineindices2()
			findlines()

			#--------------------------------------------------------------------
			for i in newdefects:
				start = i[0]
				end = i[1]
				far = i[2]
				cv2.line(finalColor,start,end,green,2)
				if(far!=-1):
					cv2.circle(finalColor,start,5,blue,-1)
					cv2.circle(finalColor,far,5,red,-1)
		
	# cv2.drawContours(finalColor,[biggestC],-1,green,2)

	cv2.imshow('finalColor', finalColor)
	cv2.imshow('fgmask',fgmask)
	cv2.imshow('eroded', eroded)
	cv2.imshow('final', final)

	k = cv2.waitKey(1) & 0xff
	if k==ord('q'):
		break
#for pt in pts:
#	for pt2 in pt:
#		print pt2
#print canny[0]
#sumed= np.concatenate(pts[0],pts[1])
print canny[0].shape
print final.shape
cv2.destroyAllWindows()