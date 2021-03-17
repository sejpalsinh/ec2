import datetime
import time
import algofirebase

class User:
	candleData = {'o':-1.1,'h':-1.1,'l':-1.1,'c':-1.1,'put':-1.1,'call':-1.1}
	def __init__(self,userType,pb,pos,price,sl,userId,password,towAuth,callFlag,callTrig,callPrice,putFlag,putTrig,putPrice):
		self.userType = userType
		self.pb = pb
		self.pos = pos
		self.price = price
		self.sl = sl
		self.userId = userId
		self.password = password
		self.towAuth = towAuth
		self.callFlag = callFlag
		self.callTrig = callTrig
		self.callPrice = callPrice
		self.putFlag = putFlag
		self.putPrice = putPrice
		self.putTrig = putTrig
		self.haveDataToUpdate = False
		self.haveLogs = False
		self.logData = "nothing"

	def printUserData(self):
		print("UserType ",self.userType)
		print("PB ",self.pb)
		print("Pos ",self.pos)
		print("Price",self.price)
		print("SL ",self.sl)
		print("UserId ",self.userId)
		print("Password ",self.password)
		print("TowAuth ",self.towAuth)
		print("callFlag",self.callFlag)
		print("callTrig",self.callTrig)
		print("callPrice",self.callPrice)
		print("putFlag",self.putFlag)
		print("putTrig",self.putTrig)
		print("putPrice",self.putPrice)

	def resetUserData(self):
		self.pb = -1.1
		self.pos = "non"
		self.price = -1.1
		self.sl = -1.1

	def addLog(self,actionUser,userType,actionTag,actionVal):
		actionTime = datetime.datetime.now()
		logMsg = str(actionUser)+","+str(userType)+","+str(actionTime)+","+str(actionTag)+","+str(actionVal)
		print(logMsg)
		self.haveLogs = True
		self.logData = logMsg

	def buyOnHighBreak(self,tickdata):
		self.pos = "bought"
		self.price = tickdata
		self.pb = tickdata + (tickdata/10)
		r2 = (tickdata - (tickdata/50))
		candleLow = self.candleData['l']
		self.sl = r2 if r2 > candleLow else candleLow
		self.callTrig = self.price - (self.price - self.sl)/2
		self.addLog(self.userId,self.userType,"Bought",tickdata)

	def sellOnLowBreak(self,tickdata):
		self.pos = "sold"
		self.price = tickdata
		self.pb = tickdata - (tickdata/10)
		r2 = (tickdata + (tickdata/50))
		candleLow = self.candleData['h']
		self.sl = r2 if r2 < candleLow else candleLow
		self.putTrig = self.price + (self.sl - self.price)/2
		self.addLog(self.userId,self.userType,"Sold",tickdata)

	def sellAndSquarOff(self,tickdata):
		valGap = tickdata-self.price
		if(valGap>0):
			self.addLog(self.userId,self.userType,"Sell SquarOff Profit",valGap)
		else:
			self.addLog(self.userId,self.userType,"Sell SquarOff Loss",valGap)
		self.resetUserData()

	def buyAndSquarOff(self,tickdata):
		valGap = self.price-tickdata
		if(valGap>0):
			self.addLog(self.userId,self.userType,"Buy SquarOff Profit",valGap)
		else:
			self.addLog(self.userId,self.userType,"Buy SquarOff Loss",valGap)
		self.resetUserData()

	def sellCall(self,tickdata):
		self.callTrig = self.candleData['h']
		self.callFlag="sold"
		self.callPrice = self.candleData['call']
		self.addLog(self.userId,self.userType,"Sold Call for ",self.callPrice)
		self.updateAlgoUserDataToDb()

	def buyCall(self,tickdata):
		self.callFlag="non"
		self.addLog(self.userId,self.userType,"Buy SquarOff Call  ",self.callPrice-self.candleData['call'])
		self.updateAlgoUserDataToDb()

	def sellPut(self,tickdata):
		self.putTrig = self.candleData['l']
		self.putFlag="sold"
		self.putPrice = self.candleData['put']
		self.addLog(self.userId,self.userType,"Sold Put for ",self.putPrice)
		self.updateAlgoUserDataToDb()

	def buyPut(self,tickdata):
		self.putFlag="non"
		self.addLog(self.userId,self.userType,"Buy SquarOff Put  ",self.putPrice-self.candleData['put'])
		self.updateAlgoUserDataToDb()

	def updateAlgoUserDataToDb(self):
		self.haveDataToUpdate = True

	def checkConditions(self,tickdata):
		if(self.pos=="non" and (self.userType=="buysellboth" or self.userType=="onlybuy") and tickdata>self.candleData['h']):
			self.buyOnHighBreak(tickdata)
			self.updateAlgoUserDataToDb()
		if(self.pos=="non" and (self.userType=="buysellboth" or self.userType=="onlysell") and tickdata<self.candleData['l']):
			self.sellOnLowBreak(tickdata)
			self.updateAlgoUserDataToDb()
		if(self.pos=="bought" and (self.userType=="buysellboth" or self.userType=="onlybuy")):
			if(tickdata>self.pb or tickdata<self.sl):
				self.sellAndSquarOff(tickdata)
			elif(tickdata<self.callTrig and self.callFlag=="non"):
				self.sellCall(tickdata)
			elif(tickdata>self.callTrig and self.callFlag=="sold"):
				self.buyCall(tickdata)
			self.updateAlgoUserDataToDb()
		if(self.pos=="sold" and (self.userType=="buysellboth" or self.userType=="onlysell")):
			if(tickdata<self.pb or tickdata>self.sl):
				self.buyAndSquarOff(tickdata)
			elif(tickdata>self.putTrig and self.putFlag=="non"):
				self.sellPut(tickdata)
			elif(tickdata<self.putTrig and self.putFlag=="sold"):
				self.buyPut(tickdata)
			self.updateAlgoUserDataToDb()

	def updateSl(self):
		if(self.pos=="bought" and self.sl<self.candleData['l']):
			self.sl = self.candleData['l']
			self.updateAlgoUserDataToDb()
		if(self.pos=="sold" and self.sl>self.candleData['h']):
			self.sl = self.candleData['h']
			self.updateAlgoUserDataToDb()

	def dataToUpDate(self):
		updateDataVal =  {
			"userType" :self.userType,
			"pb": self.pb,
			"pos": self.pos,
			"price": self.price,
			"sl": self.sl,
			"password": self.password,
			"towAuth": self.towAuth,
			"callFlag": self.callFlag,
			"callTrig": self.callTrig, 
			"callPrice": self.callPrice, 
			"putFlag": self.putFlag,
			"putPrice": self.putPrice, 
			"putTrig": self.putTrig
		}
		tempHaveDataToUpdate = self.haveDataToUpdate
		self.haveDataToUpdate = False
		return tempHaveDataToUpdate,updateDataVal

	def logsToUpdate(self):
		temphaveLogs = self.haveLogs
		self.haveLogs = False
		return temphaveLogs,self.logData

usersList = []

def setupAllUsersData(algoName):
	usersData = algofirebase.getAlogUsersData(algoName)
	for userId,userData in usersData.items():
		userType = userData['userType']
		pb = userData['pb']
		pos = userData['pos']
		price = userData['price']
		sl = userData['sl']
		password = userData['password']
		towAuth = userData['towAuth']
		callFlag = userData['callFlag']
		callTrig = userData['callTrig']
		callPrice = userData['callPrice']
		putFlag = userData['putFlag']
		putTrig = userData['putTrig']
		putPrice = userData['putPrice']
		usersList.append(User(userType,pb,pos,price,sl,userId,password,towAuth,callFlag,callTrig,callPrice,putFlag,putTrig,putPrice))

def printAllUSerData():
	for user in usersList:
		user.printUserData()

def updateUserDataToDatabase():
	allUsersUpdateData = {}
	updateFirebase = False
	for user in usersList:
		needUpdate,updateVal = user.dataToUpDate()
		if(needUpdate==True):
			updateFirebase = True
			allUsersUpdateData[user.userId] = updateVal
	if(updateFirebase==True):
		algofirebase.updateDataInUser("r2r10",allUsersUpdateData)

def updateUserLogsToDatabase():
	alluserLogs = []
	updateFirebase = False
	for user in usersList:
		needUpdate,updateVal = user.dataToUpDate()
		if(needUpdate==True):
			updateFirebase = True
			alluserLogs.append(updateVal)
	if(updateFirebase==True):
		algofirebase.updateLogsInUser("r2r10",alluserLogs)

def checkUserDataConditions(tickdata):
	for user in usersList:
		user.checkConditions(tickdata)
	updateUserDataToDatabase()
	updateUserLogsToDatabase()

def updateSlOfUsers():
	for user in usersList:
		user.updateSl()

def setFakeData():
	for user in usersList[:-1]:
		user.callFlag = "done"
		user.haveDataToUpdate = True

setupAllUsersData("r2r10")
printAllUSerData()


