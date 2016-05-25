import cv2
faceCascade = cv2.CascadeClassifier('faceCascade.xml')

cam = cv2.VideoCapture(0)
print "Press 'q' to exit."
while True:
	ret,frame = cam.read()
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

	faces = faceCascade.detectMultiScale(
		gray,
		scaleFactor = 1.3,
		minNeighbors = 5,
		minSize = (30,30),
		)

	for (x,y,w,h) in faces:
		cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

	cv2.imshow('Face Recognition', frame)
	if(cv2.waitKey(1) & 0xFF == ord('q')):
		break

cam.release()
cv2.destroyAllWindows()