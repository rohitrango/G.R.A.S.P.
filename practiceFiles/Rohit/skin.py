import cv2, numpy as np 
cam = cv2.VideoCapture(0)

def nothing(x):
	pass 

lowH,lowS,lowV = 5,38,51
highH,highS,highV = 17,250,242

while True:
	_, frame = cam.read()
	frame = cv2.flip(frame,90)
	hsvFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	# cv2.namedWindow('trackbars')
	
	# cv2.createTrackbar('lowH','trackbars',5,255,nothing)
	# cv2.createTrackbar('lowS','trackbars',38,255,nothing)
	# cv2.createTrackbar('lowV','trackbars',51,255,nothing)
	# cv2.createTrackbar('highH','trackbars',17,255,nothing)
	# cv2.createTrackbar('highS','trackbars',250,255,nothing)
	# cv2.createTrackbar('highV','trackbars',242,255,nothing)

	# lowH = cv2.getTrackbarPos('lowH','trackbars')
	# lowS = cv2.getTrackbarPos('lowS','trackbars')
	# lowV = cv2.getTrackbarPos('lowV','trackbars')
	# highH = cv2.getTrackbarPos('highH','trackbars')
	# highS = cv2.getTrackbarPos('highS','trackbars')
	# highV = cv2.getTrackbarPos('highV','trackbars')

	lSkin = np.array([lowH,lowS,lowV])
	uSkin = np.array([highH,highS,highV])

	# hsvFrame = cv2.GaussianBlur(hsvFrame,(7,7),1,1)
	skinMask = cv2.inRange(hsvFrame,lSkin,uSkin)
	skinMasked = cv2.bitwise_and(hsvFrame,hsvFrame,mask=skinMask)
	skinMasked = cv2.cvtColor(skinMasked,cv2.COLOR_HSV2BGR)
	skinMasked = cv2.cvtColor(skinMasked,cv2.COLOR_BGR2GRAY)
	_,skinMasked = cv2.threshold(skinMasked,60,255,cv2.THRESH_BINARY)
	
	finalSkin = cv2.morphologyEx(skinMasked,cv2.MORPH_ERODE,np.ones((3,3),dtype=np.uint8),iterations=2)
	finalSkin = cv2.morphologyEx(finalSkin,cv2.MORPH_OPEN,np.ones((5,5), dtype=np.uint8),iterations=1)
	finalSkin = cv2.morphologyEx(finalSkin,cv2.MORPH_CLOSE,np.ones((9,9),dtype=np.uint8),iterations=1)
	finalSkin = cv2.medianBlur(finalSkin,11)
	cv2.imshow('skinMasked',skinMasked)
	cv2.imshow('finalSkin', finalSkin)

	k = cv2.waitKey(1)
	if k==ord('q'):
		break

cam.release()
cv2.destroyAllWindows()