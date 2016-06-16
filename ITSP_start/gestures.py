import functions
from math import fabs
import os
prevPoint = None
nextPoint = None
ctr = 1

def recordGesture():
	global ctr
	if(prevPoint!=None and nextPoint!=None):
		# find the rel positions
		if(functions.P2P(prevPoint,nextPoint)>1):
			acc = 2
			xdist = nextPoint[0] - prevPoint[0]
			ydist = nextPoint[1] - prevPoint[1]
			cmd = "xdotool mousemove_relative -- " + str(acc*xdist) + " " + str(acc*ydist)
			os.system(cmd)

			'''
			xdist = fabs(nextPoint[0]-prevPoint[0])
			ydist = fabs(nextPoint[1]-prevPoint[1])
			print ctr
			if xdist>ydist:
				if(nextPoint[0] > prevPoint[0] and xdist>30):
					print "Right"
				else:
					print "Left"
			else:
				if(nextPoint[1]>prevPoint[1] and ydist>30):
					print "Down"
				else:
					print "Up"
				print "\n\n"
				ctr+=1
			'''