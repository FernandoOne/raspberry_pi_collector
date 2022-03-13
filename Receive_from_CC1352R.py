from datetime import datetime

class receiveData:
    def __init__(self):
        self.endOfTheSensorData = 0
        self.moreDataLeft = 0

    def processReading(self, serialString):
        self.endOfTheSensorData = 0
        self.moreDataLeft = 0
        sensorsData = []
        #See if there is data from the sensors
        self.moreDataLeft = serialString.find("Device Status", self.endOfTheSensorData)
        while self.moreDataLeft != -1:
            #Read the data from one sensor
            sensorData = serialString[(serialString.find("Device Status", self.endOfTheSensorData)) : (serialString.find("RSSI", self.endOfTheSensorData) + 8)]
            #Get the position where the data from the sensor read finishes
            self.endOfTheSensorData = serialString.find("RSSI", self.endOfTheSensorData) + 8
            #See if there is more data left from the sensors
            self.moreDataLeft = serialString.find("Device Status", self.endOfTheSensorData)
            #Add time stamp
            sensorData = sensorData + " Time=" + datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
            #Append it to the list of sensor data
            sensorsData.append(sensorData)
        return sensorsData
