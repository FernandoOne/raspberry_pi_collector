#Initialize the serial port

import serial
from datetime import datetime

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
def main():

    serialString = ""  # Used to hold data coming over UART
    while 1:

        #input()

        if Menu.getSendActionFlag() == False:

            print("Ingrese una acción:")

            key = input()

            if key == "1":

                Menu.sendAction("FORM_NETWORK")
            
            if key == "2":

                Menu.sendAction("OPEN_NETWORK")

            if key == "3":

                Menu.sendAction("CLOSE_NETWORK")  

            if key == "4":

                Menu.sendAction("SET_REPORT_INTERVAL", b'\033[C') 


        if Menu.getSendActionFlag() == True:
            if Menu.getAlreadySentFlag() == False:
                Menu.processWriting(serialPort)

        # Wait until there is data waiting in the serial buffer
        while serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline()

            try:

                outputString = serialString.decode("Ascii")

                print(outputString)         
    
                if Menu.getSendActionFlag() == True:
                    if Menu.getEndOfStep0String() in outputString:
                        Menu.setMenuStep(1)
                    if Menu.getEndOfStep2String() in outputString:
                        Menu.setMenuStep(3)
                Menu.setAlreadySentFlag(False)

                outputString = ""

            except:
                pass

if __name__ == '__main__':
    main()
