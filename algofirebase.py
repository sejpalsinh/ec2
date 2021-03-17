import pyrebase

config = {
  "apiKey": "ho2ZcMxFPgCtcx4rmjoDdiZ1VziePlNOtmggURu2",
  "authDomain": "Algotrade.firebaseapp.com",
  "databaseURL": "https://algotrade-a2ad6-default-rtdb.firebaseio.com/",
  "storageBucket": "Algotrade.appspot.com"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

def updateAlgoUserData(algoName,userId,fieldName,fieldData):
	db.child("algorithms").child(algoName).child("users").child(userId).child(fieldName).set(fieldData)


def getAlogUsersData(algoName):
	return db.child("algorithms").child(algoName).child("users").get().val()

def addLogToAlgo(algoName,logmsg):
	lognumber = int(db.child("algorithms").child(algoName).child("zlogs").child("totallogs").get().val())+1
	db.child("algorithms").child(algoName).child("zlogs").child(lognumber).set(logmsg)
	db.child("algorithms").child(algoName).child("zlogs").child("totallogs").set(lognumber)

def addFakeUsers(userId,userData):
	dataToAdd = {}
	dataVal =  {
		"userType" : userData['userType'],
		"pb": userData['pb'],
		"pos": userData['pos'],
		"price": userData['price'],
		"sl": userData['sl'],
		"password": userData['password'],
		"towAuth": userData['towAuth'],
		"hashFlag": userData['hashFlag'],
		"hashTrig": userData['hashTrig'],
		"hashPrice": userData['hashPrice']
	}
	dataToAdd[userId] = dataVal
	db.child("algorithms").child("r2r10").child("users").update(dataToAdd)

def updateDataInUser(algoName,dataToUpdate):
	db.child("algorithms").child("r2r10").child("users").update(dataToUpdate)

def updateLogsInUser(algoName,dataToUpdate):
	lognumber = int(db.child("algorithms").child(algoName).child("zlogs").child("totallogs").get().val())
	logsData = {}
	for lo in dataToUpdate:
		lognumber = lognumber+1
		logsData[lognumber] = lo
	db.child("algorithms").child(algoName).child("zlogs").update(logsData)
	db.child("algorithms").child(algoName).child("zlogs").child("totallogs").set(lognumber)

