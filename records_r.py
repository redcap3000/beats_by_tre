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

showOutput = True

def adjustTimeBySeconds(time, delta):
    return time + datetime.timedelta(seconds=delta)

def getKeys():
	rScan = Redis.scan(0)
	hasCursor = True
	cursor = int(0)
	while hasCursor:
		print("\nScanning\t" + str(cursor))
		rScan = Redis.scan(cursor)
		cursor = rScan[0]
		for i in range(len(rScan[1])):
			print(rScan[1][i])
			record = Redis.hgetall(rScan[1][i])
			print(record)				

def getRRecord():
	time = datetime.datetime.now()
	str(time.time())
	##print(int(adjustTimeBySeconds(time,1).strftime("%s")))
	print(adjustTimeBySeconds(time,1))
	rKey = str(adjustTimeBySeconds(time,1))
	
	return Redis.hmget(rKey,'d')	
## main loop
while True:
	getKeys()
	#print(getRRecord())
