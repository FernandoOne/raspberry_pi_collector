import time
import platform

########################################################################
#Initialize the serial port

import serial

if platform.system() == "Windows":
    portName = "COM7"
elif platform.system() == "Linux":
    portName = "/dev/ttyACM0"

serialPort = serial.Serial(port=portName, baudrate=115200, bytesize=8, timeout=0.01, stopbits=serial.STOPBITS_ONE)

#Custom functions to communicate with the board

from Send_to_CC1352R import *
menu = menuNavigation()

from Receive_from_CC1352R import *
data = receiveData()

########################################################################
#MQTT communication

import paho.mqtt.client as mqtt

flag_connected = 0

def on_connect(client, userdata, flags, rc):
   global flag_connected
   flag_connected = 1
   print('connected (%s)' % client._client_id)
   client.subscribe(topic='actions_789/', qos=2)

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
    print(parameter)
    menu.sendAction(action, parameter)

client = mqtt.Client(client_id='RaspberryPi', clean_session=True)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.connect(host='test.mosquitto.org', port=1883)
client.loop_start()

########################################################################
#Main script

def main():

    serialString = ""  # Used to hold data coming over UART
    while 1:

        #Process the writing to the board
        if menu.getSendActionFlag() == True:
            if menu.getAlreadySentFlag() == False:
                menu.processWriting(serialPort)

        # Wait until there is data waiting in the serial buffer
        while serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found.
            serialString = serialPort.readline().decode("Ascii")

            try:
                #Get the data from the sensors, if there is any
                sensorsData = data.processReading(serialString)

                #Send data to Mosquitto
                for sensorData in sensorsData:   
                    if flag_connected == 0:
                        client.connect(host='test.mosquitto.org', port=1883)
                    client.publish("hum_node_789/", sensorData, 2)
                    time.sleep(0.05)
                    print(sensorData)

                #Process data from the menus
                if menu.getSendActionFlag() == True:
                    menu.postProcessWriting(serialString)

                serialString = ""
            
            except:
                serialString = ""

if __name__ == '__main__':
	main()
