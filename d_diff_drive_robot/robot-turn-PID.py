import diff_drive
import pid_include as pid
import ach
import sys
import time
import numpy as np
from ctypes import *


dd = diff_drive
tim = dd.H_TIME()

ROBOT_TIME_CHAN  = 'robot-time'

t = ach.Channel(ROBOT_TIME_CHAN)
t.flush()

p = ach.Channel(pid.PID_REF_NAME)
PIDout = pid.PID_REF()

lastTime = 0
Input = 0.0
lastInput = 0.0
Output = 0.0
setPoint = 0.0
errSum = 0.0
#lastError = 0.0
kp = 0.0
ki = 0.0
kd = 0.0

sampleRate = 50000 #microseconds

while(1):
	[status, framesize] = t.get(tim, wait=False, last=True)
	if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
		pass
		#print 'Sim Time = ', tim.sim[0]
	else:
		raise ach.AchException( v.result_string(status) )
	dt = tim.sim[0] - lastTime #delta T, change in time
	error = setPoint - Input 
	errSum += (error*dt) #integral of error
#	dErr = (error - lastError) / dt #delta error, change in error
	dInput = (Input - lastInput)/dt #derivative of input; use this to avoid spikes at new setpoints
#	Output = (kp*error) + (ki*errSum) + (kd*dErr)
	Output = (kp*error) + (ki*errSum) - (kd*dInput)
	
#	lastError = error
	lastInput = Input
	lastTime = tim.sim[0]

	[status, framesize] = t.get(tim, wait=False, last=True)
	if status == ach.ACH_OK or status == ach.ACH_MISSED_FRAME or status == ach.ACH_STALE_FRAMES:
		pass
		#print 'Sim Time = ', tim.sim[0]
	else:
		raise ach.AchException( v.result_string(status) )
	usleep(sampleRate - (tim.sim[0] - lastTime))
