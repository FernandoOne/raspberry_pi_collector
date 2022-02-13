#Initialize the serial port

import serial
from datetime import datetime

import time

from Send_to_CC1352R import *

serialPort = serial.Serial(port="COM7", baudrate=115200, bytesize=8, timeout=0.01, stopbits=serial.STOPBITS_ONE)

#Initialize MQTT communication

import paho.mqtt.client as mqtt

flag_connected = 0

def on_connect(client, userdata, flags, rc):
   global flag_connected
   flag_connected = 1

def on_disconnect(client, userdata, rc):
   global flag_connected
   flag_connected = 0

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.connect(host='127.0.0.1', port=1883)

#Main script

action = "Form network"

def main():

    sendDataFlag = "False"
    menuStep = "0"
    alreadySent = "False"

    serialString = ""  # Used to hold data coming over UART
    while 1:

        data = OPEN_NETWORK
        sendDataFlag = "True"

        if sendDataFlag == "True":
            if alreadySent == "False":
                menuStep = processDataToSend(data, menuStep, serialPort)      
                alreadySent = "True"

        # Wait until there is data waiting in the serial buffer
        while serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline()

            try:

                outputString = serialString.decode("Ascii")

                print(outputString)

                #time.sleep(0.05)              
    
                if menuStep != "4":
                    if "<   NETWORK ACTIONS   >" in outputString:
                        menuStep = "1"

                    if "<       OPEN NWK      >" in outputString:
                        menuStep = "3"

                outputString = ""

                print(outputString)
                    
                alreadySent = "False"

            except:
                pass

if __name__ == '__main__':
    main()
