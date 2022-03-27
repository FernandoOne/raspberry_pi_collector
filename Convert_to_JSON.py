import json

#This function is used to convert the data obtained from the sensor to JSON format
def convertSensorDataStringToJSON(dataString):

    dataList = dataString.split("=")
    for i in range(0, len(dataList)):
        dataList[i] = dataList[i].split(",")

    dataDictionary = {}
    dataDictionary["Address"] = dataList[1][0]
    dataDictionary["Temperature"] = dataList[2][0]
    dataDictionary["Humidity"] = dataList[3][0]
    dataDictionary["Light"] = dataList[4][0]
    dataDictionary["RSSI"] = dataList[5][0]
    dataDictionary["Time"] = dataList[6][0]

    dataJSON = json.dumps(dataDictionary, indent = 4)

    return dataJSON
