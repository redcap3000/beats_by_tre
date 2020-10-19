import os
import time
import datetime
from decimal import *

from sense_hat import SenseHat

sense = SenseHat()
sense.set_imu_config(False, False, True)

##getcontext().prec = 32
global isHundy,ifHundy,showOutput

showOutput = True
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
	return os.system('tplink-smarthome-api blink ' + tpHost + ' ' + str(blinkCount) + ' ' + str(blinkRate)+ '&')


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
		tpBlink('10.0.0.2',2,1)
		##os.system('tplink-smarthome-api blink 10.0.0.2 3 .5&')
	## uhhh do this better plz.
	elif (xOutput == '*' and yOutput == '*') or (yOutput == '*' and zOutput == '*') or (xOutput =='*' and yOutput == '*'):
		tpBlink('10.0.0.2',1,0)
		os.system('tplink-smartphone-api blink ' + tpHost + ' ' + str(tpBlinkCount) + str(tpBlinkRate))
	
	if showOutput:
		print(  '|' + xOutput +  zOutput +  yOutput)
	## data insert
	##insertRRecord(xOutput,zOutput,yOutput,d['x'],d['y'],d['z'])

## main loop
while True:
	try:
		## check for keypress to toggle output display
		formAccelData(accel)
		## use query to show when last '!!!' occured
	except NameError:
		accel = sense.get_accelerometer_raw()
