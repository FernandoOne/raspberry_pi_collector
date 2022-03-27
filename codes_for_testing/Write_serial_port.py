#Initialize the serial port

import serial
from datetime import datetime

from Send_to_CC1352R import *

menu = menuNavigation()

serialPort = serial.Serial(port="COM7", baudrate=115200, bytesize=8, timeout=0.01, stopbits=serial.STOPBITS_ONE)

#Initialize MQTT communication

import paho.mqtt.client as mqtt

flag_connected = 0

def on_connect(client, userdata, flags, rc):
   global flag_connected
   flag_connected = 1
   print('connected (%s)' % client._client_id)
   client.subscribe(topic='actions/', qos=2)

def on_disconnect(client, userdata, rc):
   global flag_connected
   flag_connected = 0

def on_message(client, userdata, message):
    message = str(message.payload)
    if "," in message:
        [action, parameter] = message.split(",")
    else:
        action = message
        parameter = ""
    print(action)
    menu.sendAction(action, parameter)

client = mqtt.Client(client_id='RaspberryPi_', clean_session=True)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.connect(host='127.0.0.1', port=1883)
client.loop_start()

#Main script
def main():

    serialString = ""  # Used to hold data coming over UART
    while 1:

        if menu.getSendActionFlag() == False:

            print("Ingrese una acción:")

            key = input()

            if key == "1":

                menu.sendAction("FORM_NETWORK")
            
            if key == "2":

                menu.sendAction("OPEN_NETWORK")

            if key == "3":

                menu.sendAction("CLOSE_NETWORK")  

            if key == "4":

                menu.sendAction("SET_REPORT_INTERVAL", "00010000") 

        if menu.getSendActionFlag() == True:
            if menu.getAlreadySentFlag() == False:
                menu.processWriting(serialPort)

        # Wait until there is data waiting in the serial buffer
        while serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline()

            try:

                outputString = serialString.decode("Ascii")

                print(outputString)         

                if menu.getSendActionFlag() == True:
                    menu.postProcessWriting(outputString)

                outputString = ""

            except:
                pass

if __name__ == '__main__':
    main()
