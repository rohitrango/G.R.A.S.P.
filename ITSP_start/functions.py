import math

green = (0,255,0)
blue = (255,0,0)
red = (0,0,255)
yellow = (0,255,255)

def P2P(a,b):
	try:
		return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
	except:
		print "a or b is NoneType"
		return 0

def angle(a,b,c):
	return math.fabs(math.atan2(a[1]-b[1], a[0]-b[0]) - math.atan2(c[1]-b[1],c[0]-b[0]) ) 
