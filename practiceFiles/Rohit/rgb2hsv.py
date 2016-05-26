import cv2, numpy as np
r = input("Red- ")
g = input("Green- ")
b = input("Blue- ")

rgb = np.uint8([[[r,g,b]]])
hsv = cv2.cvtColor(rgb,cv2.COLOR_BGR2HSV)
print hsv

# After getting the HSV value for a color value
# Take the color range as [H-10,50,50] (lower value) to [H+10,255,255] (upper value)
# apply the mask accordingly