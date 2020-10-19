import time
import datetime
from decimal import *

from sense_hat import SenseHat



import subprocess
import os
## python 2.7 'hack' for supressing cli output and running commands in background
## should eventually develop a queue to avoid sending blink commands at more than
## once per second, but ideally not more than three times per four seconds (so each blink
## can have a chance of registering)

def subProcTry(cmd,arg1,arg2,arg3,arg4):
	try:
		with open(os.devnull, 'w') as fp:
		
			completed = subprocess.Popen([str(cmd),str(arg1),str(arg2),str(arg3),str(arg4)],stdout=fp)
	except subprocess.CalledProcessError as err:
		print('ERROR:',err)	

sense = SenseHat()
sense.set_imu_config(False, False, True)

##getcontext().prec = 32
global isHundy,ifHundy,showOutput

showOutput = False
isHundy = False

def get_change(current, previous):
    if current == previous:
        return 100.0
    try:
        return (abs(current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return 0

def get_sense_data():
	accel = sense.get_accelerometer_raw()
	return accel


def ifHundy(n,rawN):
	if n == '100' :
		isHundy = True
		return '*'
	elif '{0:.0g}'.format(rawN) == '0.0':
		return '0'
	else :
		return ' ' 

def tpBlink(tpHost,blinkCount,blinkRate):
	return subProcTry('tplink-smarthome-api', 'blink', tpHost, blinkCount, blinkRate)


def formAccelData(d):
        nAccel = sense.get_accelerometer_raw()
	dFormat = '{0:.3g}'
	isHundy = False
	
	x = get_change(nAccel['x'],d['x'])
	xOutput = ifHundy(dFormat.format(x),x)
	
	y = get_change(nAccel['y'],d['y'])
	yOutput = ifHundy(dFormat.format(y),y)
	
	z = get_change(nAccel['z'],d['z'])
	zOutput = ifHundy(dFormat.format(z),z)
	
	if xOutput == '*' and zOutput == '*' and yOutput == '*':
		xOutput = '!'
		zOutput = '!'
		yOutput = '!' 
		## want to show minimal output for cpu cycles
		if showOutput:
			print('!!!')
		tpBlink('10.0.0.2',2,1)
		##tpBlink('10.0.0.10',2,1)
	## uhhh do this better plz.
	elif (xOutput == '*' and yOutput == '*') or (yOutput == '*' and zOutput == '*') or (xOutput =='*' and yOutput == '*'):
		if showOutput:
			print('!!')
		tpBlink('10.0.0.2',1,.5)
		##tpBlink('10.0.0.10',1,.5)	
	if showOutput:
		print(  '|' + xOutput +  zOutput +  yOutput)
	## data insert
	##insertRRecord(xOutput,zOutput,yOutput,d['x'],d['y'],d['z'])

## main loop
while True:
	try:
		## check for keypress to toggle output display
		formAccelData(accel)
		time.sleep(.25)
		## use query to show when last '!!!' occured
	except NameError:
		accel = sense.get_accelerometer_raw()
