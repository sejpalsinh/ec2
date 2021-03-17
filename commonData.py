import datetime
nowTime = datetime.datetime.today()

def SetHashName():
	monthName = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOT","DEC"]
	return "NFO:BANKNIFTY"+str(nowTime.year)[2:]+monthName[nowTime.month - 1]

H = -1.1
L = -1.1
ltp = -1.1
hashName = SetHashName()

def getBankNiftyTokenName():
	return hashName+"FUT"

def getHashTokenName(currentPrice,hashType):
	targetPrice = 0
	if(currentPrice%100 > 50):
		targetPrice = ((int)(currentPrice/100) + 1)*100
	else:
		targetPrice = ((int)(currentPrice/100))*100
	return hashName+str(targetPrice)+str(hashType)




