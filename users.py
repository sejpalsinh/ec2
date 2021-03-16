import datetime
import time
import algofirebase

class User:
	candleData = {'o':-1.1,'h':-1.1,'l':-1.1,'c':-1.1}
	def __init__(self,userType,pb,pos,price,sl,userId,password,towAuth,hashFlag,hashTrig,hashPrice):
		self.userType = userType
		self.pb = pb
		self.pos = pos
		self.price = price
		self.sl = sl
		self.userId = userId
		self.password = password
		self.towAuth = towAuth
		self.hashFlag = hashFlag
		self.hashTrig = hashTrig
		self.hashPrice = hashPrice

	def printUserData(self):
		print("UserType ",self.userType)
		print("PB ",self.pb)
		print("Pos ",self.pos)
		print("Price",self.price)
		print("SL ",self.sl)
		print("UserId ",self.userId)
		print("Password ",self.password)
		print("TowAuth ",self.towAuth)
		print("HashFlag",self.hashFlag)
		print("HashTrig",self.hashTrig)
		print("HashPrice",self.hashPrice)

	def resetUserData(self):
		self.pb = -1.1
		self.pos = "non"
		self.price = -1.1
		self.sl = -1.1
		self.hashFlag = "non"
		self.hashTrig = -1.1
		self.hashPrice = -1.1

	def addLog(self,actionUser,userType,actionTag,actionVal):
		actionTime = datetime.datetime.now()
		logMsg = str(actionUser)+","+str(userType)+","+str(actionTime)+","+str(actionTag)+","+str(actionVal)
		print(logMsg)
		algofirebase.addLogToAlgo("r2r10",logMsg)


	def buyOnHighBreak(self,tickdata):
		self.pos = "bought"
		self.price = tickdata
		self.pb = tickdata + (tickdata/10)
		r2 = (tickdata - (tickdata/50))
		candleLow = self.candleData['l']
		self.sl = r2 if r2 > candleLow else candleLow
		self.hashTrig = self.price - (self.price - self.sl)/2
		self.addLog(self.userId,self.userType,"Bought",tickdata)

	def sellOnLowBreak(self,tickdata):
		self.pos = "sold"
		self.price = tickdata
		self.pb = tickdata - (tickdata/10)
		r2 = (tickdata + (tickdata/50))
		candleLow = self.candleData['h']
		self.sl = r2 if r2 < candleLow else candleLow
		self.hashTrig = self.price + (self.sl - self.price)/2
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
		self.addLog(self.userId,self.userType,"Sold Call for ",tickdata)
		self.hashFlag="done"

	def sellPut(self,tickdata):
		self.addLog(self.userId,self.userType,"Sold Put for ",tickdata)
		self.hashFlag="done"

	def updateAlgoUserDataToDb(self):
		algofirebase.updateAlgoUserData("r2r10",self.userId,"pos",self.pos)
		algofirebase.updateAlgoUserData("r2r10",self.userId,"pb",self.pb)
		algofirebase.updateAlgoUserData("r2r10",self.userId,"price",self.price)
		algofirebase.updateAlgoUserData("r2r10",self.userId,"sl",self.sl)

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
			elif(tickdata<self.hashTrig and self.hashFlag=="non"):
				self.sellCall(tickdata)
			self.updateAlgoUserDataToDb()
		if(self.pos=="sold" and (self.userType=="buysellboth" or self.userType=="onlysell")):
			if(tickdata<self.pb or tickdata>self.sl):
				self.buyAndSquarOff(tickdata)
			elif(tickdata>self.hashTrig and self.hashFlag=="non"):
				self.sellPut(tickdata)
			self.updateAlgoUserDataToDb()

	def updateSl(self):
		if(self.pos=="bought" and self.sl<self.candleData['l']):
			self.sl = self.candleData['l']
			self.updateAlgoUserDataToDb()
		if(self.pos=="sold" and self.sl>self.candleData['h']):
			self.sl = self.candleData['h']
			self.updateAlgoUserDataToDb()

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
		hashFlag = userData['hashFlag'] 
		hashTrig = userData['hashTrig']
		hashPrice = userData['hashPrice']
		usersList.append(User(userType,pb,pos,price,sl,userId,password,towAuth,hashFlag,hashTrig,hashPrice))

def printAllUSerData():
	for user in usersList:
		user.printUserData()
def checkUserDataConditions(tickdata):
	for user in usersList:
		user.checkConditions(tickdata)
def updateSlOfUsers():
	for user in usersList:
		user.updateSl()

setupAllUsersData("r2r10")
printAllUSerData()


