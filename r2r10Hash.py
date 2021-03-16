import users 
import datetime
import time
from login import *

isAlgoOn = True


def timeOut():
	if(isAlgoOn==False):
		return False
	if(datetime.datetime.now().hour>15):
		print("Time Out")
		return False
	elif(datetime.datetime.now().hour==15 and datetime.datetime.now().minute>=15):
		print("Time Out")
		return False
	return True

# instument token for bank nifty
insToken = "260105"
isAlgoOn = True

def SetOneHourData(startHour,startMinute):
	print("Waiting for ",startHour," : ",startMinute)
	while (((datetime.datetime.now().hour!=startHour) or (datetime.datetime.now().minute!=startMinute)) and timeOut() ):
		time.sleep(0.5)
	nowTime = datetime.datetime.now()
	tickCall = 0
	print(nowTime) # will print strting time
	afterHourTime = nowTime  + datetime.timedelta(minutes = 0)
	users.User.candleData['o'] = kite.ltp(insToken)[insToken]['last_price']
	users.User.candleData['h'] = 35395.95#users.User.candleData['o']
	users.User.candleData['c'] = users.User.candleData['o']
	users.User.candleData['l'] = 34952.85#users.User.candleData['o']
	print("Tacking Candle data till :",afterHourTime)
	while(nowTime < afterHourTime and timeOut()):
		tickCall = tickCall+1
		tickData = kite.ltp(insToken)[insToken]['last_price']
		if(tickData > users.User.candleData['h']):
			users.User.candleData['h'] = tickData
		elif(tickData < users.User.candleData['l']):
			users.User.candleData['l'] = tickData
		users.User.candleData['c'] = tickData
		time.sleep(0.2)
		users.checkUserDataConditions(tickData)
		nowTime = datetime.datetime.now()
	users.updateSlOfUsers()
	mylogstr = str(datetime.datetime.now())+",Day frist hour OHLC,"+str(users.User.candleData)
	print(mylogstr)

def StartCycle():
	tempdata = -1.1
	print("Main Alog  Started")
	while timeOut():
		tickdata = kite.ltp(insToken)[insToken]['last_price']
		if(tempdata!=tickdata):
			tempdata = tickdata
			users.checkUserDataConditions(tickdata)
		time.sleep(0.2)
	print("Main Algo Ended Started")


SetOneHourData(11,56)
StartCycle()


