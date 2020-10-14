import redis
global Redis,redis_host,redis_port,redis_password

redis_host = "localhost"
redis_port = 6379
redis_password = ""

try:
	Redis = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
except Exception as e:
        print(e)



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

def insertRRecord(x,y,z,xRaw,yRaw,zRaw):
	rKey = str(time.time())
	return Redis.hmset(rKey, {"t":rKey,"x":xRaw,"y":yRaw,"z":zRaw,"d":x+y+z})	
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
	insertRRecord(xOutput,zOutput,yOutput,d['x'],d['y'],d['z'])

## main loop
while True:
	try:
		## check for keypress to toggle output display
		formAccelData(accel)
		## use query to show when last '!!!' occured
	except NameError:
		accel = sense.get_accelerometer_raw()
