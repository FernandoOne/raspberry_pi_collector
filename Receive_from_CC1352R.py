from datetime import datetime
from Convert_to_JSON import *

class receiveData:
    def __init__(self):
        self.endOfTheSensorData = 0

    def isThereDataFromTheSensors(self, serialString):
        if (serialString.find("Device Status", self.endOfTheSensorData) != -1) and (serialString.find("RSSI", self.endOfTheSensorData) != -1) :
            return True
        else:
            return False

    def processReading(self, serialString):
        self.endOfTheSensorData = 0
        sensorsData = []
        #See if there is data from the sensors
        while self.isThereDataFromTheSensors(serialString) == True:
            #Read the data from one sensor
            sensorData = serialString[(serialString.find("Device Status", self.endOfTheSensorData)) : (serialString.find("RSSI", self.endOfTheSensorData) + 8)]
            #Get the position where the data from the sensor read finishes
            self.endOfTheSensorData = serialString.find("RSSI", self.endOfTheSensorData) + 8
            #Add time stamp
            sensorData = sensorData + ", Time=" + datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
            #Convert data to JSON
            sensorData = convertSensorDataStringToJSON(sensorData)
            #Append it to the list of sensor data
            sensorsData.append(sensorData)
        return sensorsData
