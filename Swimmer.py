class Swimmer:

    def __init__(self, name, gender, age, status):
        self._name = name
        self._gender = gender
        self._age = age
        self._status = status
        self._record = {"Event" : [], "Time" : [], "Meet" : [], "RecStatus" : []}

    def getName(self):
        return self._name
    
    def getGender(self):
        return self._gender
    
    def getAge(self):
        return self._age
    
    def getStatus(self):
        return self._status
    
    def setStatus(self, status):
        self._status = status

    def addRecord(self, event, timing, meet, recStatus):
        
        self._record.get("Event").append(event)
        self._record.get("Time").append(timing)
        self._record.get("Meet").append(meet)
        self._record.get("RecStatus").append(recStatus)    

    def getRecord(self):
        return self._record

    def getAllTimingRec(self):
        allTimingsRec = {"Event" : [], "Time" : [], "Meet" : []}
        for keyEvent in allTimingsRec.keys():
            allTimingsRec[keyEvent] = self._record.get(keyEvent)
            
        return allTimingsRec

    def getFilteredTiming(self, event):
        filteredTiming = {"Event" : [], "Time" : [], "Meet" : []}
        eventList = self._record.get("Event")
        for index in range(len(eventList)):
            if event == eventList[index]:
                filteredTiming.get("Event").append(event)
                filteredTiming.get("Time").append(self._record["Time"][index])
                filteredTiming.get("Meet").append(self._record["Meet"][index])
        return filteredTiming

    def getSwimmerInfo(self):
        return self._name + "," + self._gender + "," + str(self._age) + "," + self._status + "\n"

    
    




    



