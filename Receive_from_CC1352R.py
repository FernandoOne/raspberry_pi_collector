from datetime import datetime

class receiveData:
    def __init__(self):
        self.endOfTheSensorData = 0
        self.moreDataLeft = 0

    def processReading(self, serialString):
        try:
            self.endOfTheSensorData = 0
            self.moreDataLeft = 0
            sensorsData = []
            #See if there is data from the sensors
            if (serialString.find("Device Status", self.endOfTheSensorData) != -1) and (serialString.find("RSSI", self.endOfTheSensorData) != -1):
                self.moreDataLeft = 1
            else:
                self.moreDataLeft = -1
            print("BBBBBB")
            while self.moreDataLeft != -1:
                print("CCCCCC")
                print(self.moreDataLeft)
                if serialString.find("RSSI", self.endOfTheSensorData) != -1:
                    print("DDDDDD")
                    if serialString.find("Device Status", self.endOfTheSensorData) != -1:
                        print("EEEEEEE")
                        #Read the data from one sensor
                        sensorData = serialString[(serialString.find("Device Status", self.endOfTheSensorData)) : (serialString.find("RSSI", self.endOfTheSensorData) + 8)]
                        #Get the position where the data from the sensor read finishes
                        print("FFFFFFF")
                        self.endOfTheSensorData = serialString.find("RSSI", self.endOfTheSensorData) + 8
                        #See if there is more data left from the sensors
                        print("GGGGGGG")
                        if (serialString.find("Device Status", self.endOfTheSensorData) != -1) and (serialString.find("RSSI", self.endOfTheSensorData) != -1):
                            self.moreDataLeft = 1
                        else:
                            self.moreDataLeft = -1
                        #Add time stamp
                        sensorData = sensorData + " Time=" + datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
                        print("HHHHHH")
                        #Append it to the list of sensor data
                        sensorsData.append(sensorData)
            return sensorsData
        except:
            return []