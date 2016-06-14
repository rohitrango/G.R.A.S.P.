import functions
from math import fabs
prevPoint = None
nextPoint = None

def recordGesture():

	if(prevPoint!=None and nextPoint!=None):
		# find the rel positions
		if(functions.P2P(prevPoint,nextPoint)>50):
			if(nextPoint[0] > prevPoint[0] and fabs(nextPoint[0]-prevPoint[0])>30):
				print "Right"
			else:
				print "Left"

			if(nextPoint[1]>prevPoint[1] and fabs(nextPoint[1]-prevPoint[1])>30):
				print "Down"
			else:
				print "Up"
			print "\n\n"

