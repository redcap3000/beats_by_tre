## For using the accelerometer to detect seisemic activity that is (probably) coming from a loud stereo
## the idea is to limit the amount of output shown to give an idea of min/max tolerances
## ideally when it is triggered permit a seconds of 'lets check this sound out' to show all data
## and to hide data that isn't 'moving much'
## I think the 'ideal' location would be somewhere that does not receive a lot of vibrations from the room that it is in, but should be receving 'external' vibrations.
## reguardless of where it is placed it should be on or near the floor on a hard surface.
## kind of based on a 'wah' moment i.e. notating periods of identical readings (rare) 
## completely not based on any sort of science but from sensations on my feet
import time
import datetime
from decimal import *

from sense_hat import SenseHat

sense = SenseHat()
sense.set_imu_config(False, False, True)


import pymongo

accelDict = {
	'   ' : 0,
	'*  ' : 1,
        ' * ' : 2,
	'  *' : 3,
	'** ' : 4,
	' **' : 5,
	'* *' : 6,
	'!'   : 7
}

##getcontext().prec = 32
global isHundy,ifHundy,prevTime,myclient,mydb,mycol,showOutput

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Beats_by_tre"]
mycol = mydb["sense_accel_diff"]
showOutput = True
isHundy = False

def insertRecord(x,y,z,xRaw,yRaw,zRaw):

	##mycol2= mydb["sense_accel_raw"]
	timestamp = datetime.datetime.utcnow() 
	##accelDict[compAccel]
	if x == '!' and y == '!' and z == '!':
		y = ''
		z = ''
	return mycol.insert_one({"t":timestamp,"d":x+y+z,"x":xRaw,"y":yRaw,"z":zRaw})
	##r2 = mycol2.insert_one({"t":timestamp,"x":xRaw,"y":yRaw,"z":zRaw})


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


##def determineSymbol(axis,value):
	## TODO>?!
##	if axis == 'x':
##	elif axis == 'y':
##	elif axis == 'z':
##	return value

def ifHundy(n,rawN):
	if n == '100' :
		isHundy = True
		return '*'
	elif '{0:.0g}'.format(rawN) == '0.0':
		return '0'
	else :
		return ' ' 
		##return '{0:.3g}'.format(rawN)

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
	## uhhh do this better plz.
	if showOutput:
		print(  '|' + xOutput +  zOutput +  yOutput)
	## data insert
	insertRecord(xOutput,zOutput,yOutput,d['x'],d['y'],d['z'])

## todo 
## main loop
while True:
	try:
		## check for keypress to toggle output display
		formAccelData(accel)
		## use query to show when last '!!!' occured
	except NameError:
		accel = sense.get_accelerometer_raw()
