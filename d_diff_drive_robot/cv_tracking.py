import diff_drive
import ach
import sys
import time
from ctypes import *
import socket
import cv2.cv as cv
import cv2
import numpy as np
import operator
import cv_tracking_include as cvti


dd = diff_drive
tim = dd.H_TIME()

ROBOT_CHAN_VIEW   = 'robot-vid-chan'
ROBOT_TIME_CHAN  = 'robot-time'
CV_REF_CHAN = cvti.CV_REF_NAME

cv.NamedWindow("wctrl", cv.CV_WINDOW_AUTOSIZE)

tracked = False

#constants
newx = 320
newy = 240
nx = 640
ny = 480
center_screen = (nx/2,ny/2)
h_green = 60
h_thresh = 10
lower_green = np.zeros((ny, nx, 3), np.uint8)
upper_green = np.zeros((ny, nx, 3), np.uint8)
lower_green[:] = (h_green-h_thresh,50,50)
upper_green[:] = (h_green+h_thresh,255,255)
error = (0,0)

v = ach.Channel(ROBOT_CHAN_VIEW)
v.flush()
t = ach.Channel(ROBOT_TIME_CHAN)
t.flush()
cvt = ach.Channel(CV_REF_CHAN)
cvt.flush()

cvErr = cvti.CV_REF()

while True:
	# Get Frame
	img = np.zeros((newx,newy,3), np.uint8)
	c_image = img.copy()
	vid = cv2.resize(c_image,(newx,newy))
	[status, framesize] = v.get(vid, wait=False, last=True)
	if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
		vid2 = cv2.resize(vid,(nx,ny))
		img = cv2.cvtColor(vid2,cv2.COLOR_BGR2RGB)


		img2 = cv2.cvtColor(img,cv2.COLOR_RGB2HSV)
		mask = cv2.inRange(img2, lower_green, upper_green)
		m = cv2.moments(mask)

		#if the green ball is not on screen, hold on to it's last known location if there is one
		if(m['m00'] == 0.0):
			if(tracked):
				print 'last known location of center: ', object_center
				print 'last known error: ', error
		#if it is on screen, find it's location and how far it is from center
		else:
			tracked = True
			object_center = (int (m['m10']/m['m00']), int (m['m01']/m['m00']))
			error = tuple(map(operator.sub, object_center, center_screen))
			print 'current location of center: ', object_center
			print 'current error: ', error
		#draw red dot in center of the (visible part of the) object if it's still on screen
		if(tracked):
			if(m['m00'] != 0.0):
				res = cv2.circle(img, object_center, 3, (0,0,255))
		(cvErr.errX, cvErr.errY) = error
		cv2.imshow("wctrl", img)
		cv2.waitKey(10)
	else:
		raise ach.AchException( v.result_string(status) )


	[status, framesize] = t.get(tim, wait=False, last=True)
	if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
		pass
		#print 'Sim Time = ', tim.sim[0]
	else:
		raise ach.AchException( v.result_string(status) )

#	print 'Sim Time = ', tim.sim[0]
	time.sleep(0.1)

