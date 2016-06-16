import functions
import os
from math import fabs,atan2,pi
import cv2
prevPoint = None
nextPoint = None
ctr = 1
mode = "idle"			# we can have 'track', 'add', 'delete' and 'stop' modes  
trackGesture = []
addGesture = []
deleteGesture = []
gesturesHistory=[]
theta = pi/8
prevGesture=-1
fist_cascade=cv2.CascadeClassifier('fist.xml')

# direction notation, 1 is right and then onwards we have anticlockwise
def refreshHistory():
	gesturesHistory=[]
	prevPoint=None
	nextPoint=None
	#print "refresh"
def checkGesture():
	print gesturesHistory
	if(gesturesHistory==[1,4,2,3]):
		cm="firefox"
		os.system(cm)
		print "sucess"
def recordGesture():
	checkGesture()
	global ctr,gesturesHistory,prevGesture
	#fists = fist_cascade.detectMultiScale(frame, 1.3, 5)
	#if fists!=None:
		#for (x,y,w,h) in fists:
	'''	cv2.rectangle(finalColor,(x,y),(x+w,y+h),(0,0,0),2)
	refreshHistory()'''
	if mode=="idle":
		pass
		refreshHistory()
	elif mode=="track":
		if(functions.P2P(prevPoint,nextPoint)>100):
			xdist = (nextPoint[0]-prevPoint[0])
			ydist = (nextPoint[1]-prevPoint[1])

			angle = atan2(-ydist,xdist) 				# since in image, y axis is inverted
			print angle,"\n\n\n"

			if (angle>=-theta and angle<theta):
				# trackGesture.append(1)
				
				if(prevGesture!=4):
					gesturesHistory.append(4)
					prevGesture=4
					print "east"

			elif (angle>=theta and angle< 3*theta):
				# trackGesture.append(2)
				print "North east"
				if(prevGesture!=6):
					gesturesHistory.append(6)
					prevGesture=6
			elif (angle>=3*theta and angle<5*theta):
				# trackGesture.append(3)
			
				if(prevGesture!=1):
					gesturesHistory.append(1)
					print "North"
					prevGesture=1
			elif (angle>=5*theta and angle<7*theta):
				print "North west"
				if(prevGesture!=5):
					gesturesHistory.append(5)
					prevGesture=5
			elif (angle>=7*theta or angle<=-7*theta):
			
				if(prevGesture!=3):
					print "West"
					gesturesHistory.append(3)
					prevGesture=3
			elif (angle>-7*theta and angle<=-5*theta):
				print "South West"
				if(prevGesture!=7):
					gesturesHistory.append(7)
					prevGesture=7
			elif (angle>-5*theta and angle<=-3*theta):
			
				if(prevGesture!=2):
					print "South"
					gesturesHistory.append(2)
					prevGesture=2
			elif (angle>-3*theta and angle<=-theta):
				print "South East"
				if(prevGesture!=8):
					gesturesHistory.append(8)
					prevGesture=8
	
def changeGestureMode(customMode):
	global mode
	mode = customMode
	print "Entered %s mode."%customMode
# if(prevPoint!=None and nextPoint!=None):
# 		# find the rel positions
# 		if(functions.P2P(prevPoint,nextPoint)>90):
# 			xdist = fabs(nextPoint[0]-prevPoint[0])
# 			ydist = fabs(nextPoint[1]-prevPoint[1])
# 			print ctr
# 			if xdist>ydist:
# 				if(nextPoint[0] > prevPoint[0]):
# 					print "Right"
# 				else:
# 					print "Left"
# 			else:
# 				if(nextPoint[1]>prevPoint[1]):
# 					print "Down"
# 				else:
# 					print "Up"
# 				print "\n\n"
# 				ctr+=1
