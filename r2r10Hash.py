import users 
import datetime
import time
import threading
from login import *
from commonData import *

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
tokenName = getBankNiftyTokenName()
insToken =  kite.ltp(tokenName)[tokenName]['instrument_token']
isAlgoOn = True
tickData = -1.1

def setPutAndCallValue():
	print("put call data started")
	while timeOut():
		hastNama = getHashTokenName(tickData,"CE")
		users.User.candleData['call'] = kite.ltp(hastNama)[hastNama]['last_price']
		hastNama = getHashTokenName(tickData,"PE")
		users.User.candleData['put'] = kite.ltp(hastNama)[hastNama]['last_price']
		time.sleep(0.2)


def SetOneHourData(startHour,startMinute):
	global tickData
	print("Waiting for ",startHour," : ",startMinute)
	while (((datetime.datetime.now().hour!=startHour) or (datetime.datetime.now().minute!=startMinute)) and timeOut() ):
		time.sleep(0.5)
	nowTime = datetime.datetime.now()
	threading.Thread(target=setPutAndCallValue).start()
	tickCall = 0
	print(nowTime) # will print strting time
	afterHourTime = nowTime  + datetime.timedelta(minutes = 60)
	users.User.candleData['o'] = kite.ltp(insToken)[insToken]['last_price']
	users.User.candleData['h'] = users.User.candleData['o']
	users.User.candleData['c'] = users.User.candleData['o']
	users.User.candleData['l'] = users.User.candleData['o']
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


SetOneHourData(9,15)
StartCycle()


