import functions
import os
from math import fabs,atan2,pi
import cv2
from subprocess import call,Popen
import json

#get gesture data
f = open('./gesturedata.json','r')
filedata = f.read()
gestureData = json.loads(filedata)
f.close()

#module variables
prevPoint = None
nextPoint = None
ctr = 1
mode = "idle"			# we can have 'track', 'add', 'delete' and 'stop' modes  
trackGesture = []
addGesture = []
deleteGesture = []
prevGesture = -1
prevGestureName = None

currentProcess = None

#misc
theta = pi/8
fist_cascade=cv2.CascadeClassifier('fist.xml')

# direction notation, 1 is NW and then onwards we have clockwise
def refreshHistory():
	global trackGesture,addGesture,deleteGesture,prevPoint,nextPoint, prevGesture
	trackGesture = addGesture = deleteGesture = []
	prevGesture = -1
	prevPoint=None
	nextPoint=None
	#print "refresh"

def checkGesture():
	print trackGesture

def init():								#just for debugging
	global gestureData
	for g in gestureData:
		print g["gesture"], g["command"]

def StopRecording():
	# print "Recording stopped"
	global trackGesture,mode,gestureData,prevGestureName

	if mode=="idle":
		pass
	elif mode=="track":
		for g in gestureData:						
			if g["gesture"]==trackGesture:					## change some things here
				# if default gesture, perform action, else perform terminal command
				if g["default"]=="true":
					playDefaultAction(g)

				elif g["default"]=="false":				# not default, just open the process
					try:
						currentProcess = Popen(g["command"].split(" "))
					except:
						print "Invalid command."
					prevGestureName = None

				changeGestureMode("idle")
				refreshHistory()	
				break

def recordGesture():
	global ctr,addGesture,trackGesture,deleteGesture,prevGesture

	StopRecording()
	if mode=="idle":
		# print gestureData
		pass
		
	elif mode=="track":
		# print trackGesture								# remove after debug
		if(functions.P2P(prevPoint,nextPoint)>80):
			xdist = (nextPoint[0]-prevPoint[0])
			ydist = (nextPoint[1]-prevPoint[1])

			angle = atan2(-ydist,xdist) 				# since in image, y axis is inverted

			if (angle>=-theta and angle<theta):
				if(prevGesture!=4):
					trackGesture.append(4)
					prevGesture = 4
					print "East"

			elif (angle>=theta and angle< 3*theta):
				# trackGesture.append(2)
				if(prevGesture!=3):
					print "North East"
					trackGesture.append(3)
					prevGesture=3

			elif (angle>=3*theta and angle<5*theta):
				# trackGesture.append(3)
				if(prevGesture!=2):
					trackGesture.append(2)
					print "North"
					prevGesture=2

			elif (angle>=5*theta and angle<7*theta):

				if(prevGesture!=1):
					print "North west"
					trackGesture.append(1)
					prevGesture=1

			elif (angle>=7*theta or angle<=-7*theta):
				if(prevGesture!=8):
					print "West"
					trackGesture.append(8)
					prevGesture=8

			elif (angle>-7*theta and angle<=-5*theta):
				if(prevGesture!=7):
					print "South West"
					trackGesture.append(7)
					prevGesture=7

			elif (angle>-5*theta and angle<=-3*theta):
				if(prevGesture!=6):
					print "South"
					trackGesture.append(6)
					prevGesture=6

			elif (angle>-3*theta and angle<=-theta):
				if(prevGesture!=5):
					print "South East"
					trackGesture.append(5)
					prevGesture=5

			print trackGesture
	
def changeGestureMode(customMode):
	global mode
	mode = customMode
	print "Entered %s mode."%customMode
	refreshHistory()

def playDefaultAction(gesture):
	global prevGestureName,currentProcess

	## Main commands
	if(gesture["command"]=="google-chrome"):
		currentProcess = Popen(('google-chrome '+" ".join(gesture["urls"])).split(" "))
		prevGestureName = "google-chrome"

	elif(gesture["command"]=="firefox"):
		currentProcess = Popen(('firefox '+" ".join(gesture["urls"])).split(" "))
		prevGestureName = "firefox"

	elif(gesture["command"]=="rhythmbox"):
		Popen("rhythmbox-client --play".split(" "))
		prevGestureName = "rhythmbox"

	## Misc actions which are common to default actions
	elif(gesture["command"]=="volUp"):

		if(prevGestureName=="rhythmbox"):
			print "Volume increased."
			Popen("rhythmbox-client --volume-up".split(" "))

	elif(gesture["command"]=="volDown"):

		if(prevGestureName=="rhythmbox"):
			print "Volume decreased."
			Popen("rhythmbox-client --volume-up".split(" "))

	elif(gesture["command"]=="previous"):

		if prevGestureName=="rhythmbox":
			print "Playing previous song."
			Popen("rhythmbox-client --previous".split(" "))

	elif(gesture["command"]=="next"):

		if prevGestureName=="rhythmbox":
			print "Playing next song."
			Popen("rhythmbox-client --next".split(" "))

	elif(gesture["command"]=="pause"):

		if(prevGestureName=="rhythmbox"):
			print "Music paused."
			Popen("rhythmbox-client --pause".split(" "))

	elif(gesture["command"]=="play"):

		if(prevGestureName=="rhythmbox"):
			print "Music resumed."
			Popen("rhythmbox-client --play".split(" "))
					
	elif(gesture["command"]=="close"):

		if(prevGestureName=="rhythmbox"):
			print "Rhythmbox closed."
			Popen("rhythmbox-client --quit".split(" "))
			currentProcess = None

		elif prevGestureName=="google-chrome":
			try:
				currentProcess.terminate()
				print "Chrome process killed."
			except:
				print "Session doesnot exist. Did you close it by yourself?"
			currentProcess = None

		elif prevGestureName=="firefox":
			try:
				currentProcess.terminate()
				print "Firefox process killed."
			except:
				print "Session doesnot exist. Did you close it by yourself?"
			currentProcess = None

		prevGestureName = None

