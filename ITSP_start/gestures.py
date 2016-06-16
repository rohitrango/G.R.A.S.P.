import functions
from math import fabs,atan2,pi
prevPoint = None
nextPoint = None
ctr = 1
mode = "idle"			# we can have 'track', 'add', 'delete' and 'stop' modes  
trackGesture = []
addGesture = []
deleteGesture = []

theta = pi/8

# direction notation, 1 is right and then onwards we have anticlockwise

def recordGesture():
	global ctr
	if mode=="idle":
		pass
	elif mode=="track":
		if(functions.P2P(prevPoint,nextPoint)>100):
			xdist = (nextPoint[0]-prevPoint[0])
			ydist = (nextPoint[1]-prevPoint[1])

			angle = atan2(-ydist,xdist) 				# since in image, y axis is inverted
			print angle,"\n\n\n"

			if (angle>=-theta and angle<theta):
				# trackGesture.append(1)
				print "east"
			elif (angle>=theta and angle< 3*theta):
				# trackGesture.append(2)
				print "North east"
			elif (angle>=3*theta and angle<5*theta):
				# trackGesture.append(3)
				print "North"
			elif (angle>=5*theta and angle<7*theta):
				print "North west"
			elif (angle>=7*theta or angle<=-7*theta):
				print "West"
			elif (angle>-7*theta and angle<=-5*theta):
				print "South West"
			elif (angle>-5*theta and angle<=-3*theta):
				print "South"
			elif (angle>-3*theta and angle<=-theta):
				print "South East"
	
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
