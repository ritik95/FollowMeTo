## Object Follower: Main Code
## Ritik Mathur/Ritobroto Maitra

## November 2016


import sys 
sys.path.insert(0, "/usr/local/lib/python2.7/site-packages/") 
# Non-Mac OS users can remove the above lines.
import cv2
# Dependency: OpenCV 2
import numpy as np
import serial
# Dependency: PySerial. Install using pip install pyserial.
import time

ser = serial.Serial("/dev/cu.usbmodem1411",9600)
# Serial Port - Get from Arduino, changes from system to system

# Communicate with Arduino (servo angles)
def send_msg(pos):
	values = bytearray([pos])
	ser.write(values)
	time.sleep(0.050)

#initialize camera
cap = cv2.VideoCapture(1)
cv2.namedWindow('camera')

#colour palette for detecting forward movement of robot
lower_green = np.array([77,0,0])
upper_green = np.array([255,255,156])

while(1):

	_, frame = cap.read()
	img  = frame.copy()
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	#HSV Mask
	mask = cv2.inRange(hsv, lower_green, upper_green)
	# Mask Filter
	mask = cv2.erode(mask, None, iterations=2)
	# Erode - remove small disturbances
	mask = cv2.dilate(mask, None, iterations=2)
	# Dilate - try to reduce damage done by erode to actual object
	cnts = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	if len(cnts) > 0:
		c = sorted(cnts, key=cv2.contourArea,reverse=True)
		((x1,y1),radius1) = cv2.minEnclosingCircle(c[0])
		if radius1>50:								#minimum radius for detection
			cv2.circle(img, (int(x1), int(y1)), int(radius1),(0, 255, 255), 2)
			# Circle to show detection on the frame
			message = int(x1)/10
			print "Rotating! Please don't obstruct the motor now."
			print message
			send_msg(message)
			#send to arduino - angle of rotation
		if len(c)>1:
			((x2,y2),radius2) = cv2.minEnclosingCircle(c[1])
			if radius2>50:
				cv2.circle(img, (int(x2), int(y2)), int(radius2),(0, 255, 255), 2)
	cv2.imshow('camera',img)
	cv2.imshow('mask',mask)
	k = cv2.waitKey(5) & 0xFF
	if k == 27:
        	break

cv2.destroyAllWindows()
