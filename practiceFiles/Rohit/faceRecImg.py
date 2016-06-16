import cv2, sys, numpy as np

if(len(sys.argv)==2):
	cascPath = sys.argv[1]
else:
	cascPath = "faceCascade.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
image = cv2.imread('rohit.jpg')
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

faces = faceCascade.detectMultiScale(
	gray,
	scaleFactor = 1.1,
	minNeighbors = 5,
	minSize = (30,30)
	)
print "Found {0} faces!".format(len(faces))
for(x,y,w,h) in faces:
	cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)

cv2.imshow("Faces found", image)
print "Press any key to exit."
cv2.waitKey(0)
