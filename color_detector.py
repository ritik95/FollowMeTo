import sys 
sys.path.insert(0, "/usr/local/lib/python2.7/site-packages/") 
import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(1)
cv2.namedWindow('camera')

cv2.createTrackbar('h1','camera',0,255,nothing)
cv2.createTrackbar('s1','camera',0,255,nothing)
cv2.createTrackbar('v1','camera',0,255,nothing)
cv2.createTrackbar('h2','camera',0,255,nothing)
cv2.createTrackbar('s2','camera',0,255,nothing)
cv2.createTrackbar('v2','camera',0,255,nothing)

while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #hsv = frame.copy()
    # define range of blue color in HSV
    h1 = cv2.getTrackbarPos('h1','camera')
    s1 = cv2.getTrackbarPos('s1','camera')
    v1 = cv2.getTrackbarPos('v1','camera')

    h2 = cv2.getTrackbarPos('h2','camera')
    s2 = cv2.getTrackbarPos('s2','camera')
    v2 = cv2.getTrackbarPos('v2','camera')

    lower_blue = np.array([h1,s1,v1])
    upper_blue = np.array([h2,s2,v2])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    cv2.imshow('frame',frame)
    cv2.imshow('res',res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break


    print lower_blue
    print upper_blue

cv2.destroyAllWindows()



#threshhold for green : (40,55,0) to (75,200,255)
