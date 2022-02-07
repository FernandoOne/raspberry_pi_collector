#Initialize the serial port

import serial
from datetime import datetime

import time

serialPort = serial.Serial(port="COM7", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

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

# def main():

serialString = ""  # Used to hold data coming over UART
while 1:

    # Wait until there is data waiting in the serial buffer
    if serialPort.in_waiting > 0:

        # Read data out of the buffer until a carraige return / new line is found
        serialString = serialPort.readline()

        try:

            outputString = serialString.decode("Ascii")

            endOfTheString = 0
            condition = 0
            while condition != -1:

                sensorData = outputString[(outputString.find("Device Status", endOfTheString)) : (outputString.find("RSSI", endOfTheString) + 8)]

                endOfTheString = outputString.find("RSSI", endOfTheString) + 8

                condition = outputString.find("Device Status", endOfTheString)

                if (sensorData != ""):

                    now = datetime.now()
                    dt_string = now.strftime("%Y/%m/%d-%H:%M:%S")
                    sensorData = sensorData + " Time=" + dt_string

                    print(sensorData)

                    #Send data to Mosquitto
                    if flag_connected == 0:
                        client.connect(host='127.0.0.1', port=1883)

                    client.publish("sensors_data/", sensorData, 1)

                    time.sleep(0.05)
        
        except:
            pass

# if __name__ == '__main__':
# 	main()
