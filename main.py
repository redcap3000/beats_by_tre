## For using the accelerometer to detect seisemic activity that is (probably) coming from a loud stereo
## the idea is to limit the amount of output shown to give an idea of min/max tolerances
## ideally when it is triggered permit a seconds of 'lets check this sound out' to show all data
## and to hide data that isn't 'moving much'

import time
from decimal import *

from sense_hat import SenseHat
from datetime import datetime

sense = SenseHat()
datetime.now()
sense.set_imu_config(False, False, True)

getcontext().prec = 16
global isHundy,ifHundy

isHundy = False

def get_change(current, previous):
    if current == previous:
        return 100.0
    try:
        return (abs(current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return 0

def get_sense_data():
	sense_data = []
	##sense_data.append(sense.get_temperature())
	sense_data.append(sense.get_pressure())
	accel = sense.get_accelerometer_raw()
	
	##sense_data.append(sense.get_humidity())
	return accel
	return sense_data

def ifHundy(n,rawN):
	if n == '100' :
		isHundy = True
		return '*'
	elif '{0:.0g}'.format(rawN) == '0.0':
		return '-'
	else :
		return ' ' 
##		return '{0:.0g}'.format(rawN)

def formAccelData(d):
        nAccel = sense.get_accelerometer_raw()
	dFormat = '{0:.3g}'
	isHundy = False
	
	x = get_change(nAccel['x'],d['x'])
	xForm = dFormat.format(x)
	
	xOutput = ifHundy(xForm,x)

	y = get_change(nAccel['y'],d['y'])
	yForm = dFormat.format(y)

	
	yOutput = ifHundy(yForm,y)

	z = get_change(nAccel['z'],d['z'])
	zForm = dFormat.format(z)
	
	zOutput = ifHundy(zForm,z)
	##if isHundy == True :
	print( xOutput+' ' +zOutput +' ' +yOutput)
        ##else :
        ##        print(d['x'],d['y'],d['z'])	
while True:
	try:
		formAccelData(accel)
	except NameError:
		accel = sense.get_accelerometer_raw()
	##if 'accel' in globals():
	##	print('accel exists')
	##else:
	##	print('accel does not exist')
	
	time.sleep(1/1.75)
	##print(get_sense_data())

