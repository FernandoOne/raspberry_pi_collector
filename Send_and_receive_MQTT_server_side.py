import sys
import time

import paho.mqtt.client

def outputToFile(data):
    with open('data_received_through_mqtt.txt', 'a') as f:
        f.write(data+"\n")

def on_connect(client, userdata, flags, rc):
	print('connected (%s)' % client._client_id)
	client.subscribe(topic='sensors_data/', qos=2)

def on_message(client, userdata, message):
    print(message.payload)
    outputToFile(str(message.payload))

def main():
	client = paho.mqtt.client.Client(client_id='server', clean_session=False)
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(host='127.0.0.1', port=1883)
	client.loop_start()
	
	while 1:

		print("Enter an action:")
		
		key = input()

		if key == "1":

			client.publish("actions/", "FORM_NETWORK", 0)

		if key == "2":

			client.publish("actions/", "OPEN_NETWORK", 0)

		if key == "3":

			client.publish("actions/", "CLOSE_NETWORK", 0)

		if key == "4":

			Interval = "00003000"
			client.publish("actions/", "SET_REPORT_INTERVAL" + "," + Interval, 0)

		if key == "5":

			Sensor = "0001"
			client.publish("actions/", "SELECT_SENSOR" + "," + Sensor, 0)			

if __name__ == '__main__':
	main()

sys.exit(0)
