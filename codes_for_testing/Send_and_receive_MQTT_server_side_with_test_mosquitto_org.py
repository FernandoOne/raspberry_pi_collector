import sys
import time

import paho.mqtt.client

def outputToFile(data):
    with open('data_received_through_mqtt.txt', 'a') as f:
        f.write(data+"\n")

def on_connect(client, userdata, flags, rc):
	print('connected (%s)' % client._client_id)
	client.subscribe("hum_node_789/#", qos=2)
	#client.subscribe(topic='data/', qos=2)

def on_message(client, userdata, message):
    print(message.payload)
    #outputToFile(str(message.payload))

def main():
	client = paho.mqtt.client.Client(client_id='server', clean_session=False)
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(host='test.mosquitto.org', port=1883)
	client.loop_start()

	while 1:

		print("Enter an action:")
		
		key = input()

		if key == "1":

			client.publish("actions_789/", "FORM_NETWORK", 0)

		if key == "2":

			client.publish("actions_789/", "OPEN_NETWORK", 0)

		if key == "3":

			client.publish("actions_789/", "CLOSE_NETWORK", 0)

		if key == "4":
			
			print("Enter interval:")
			Interval = input()
			client.publish("actions_789/", "SET_REPORT_INTERVAL" + "," + Interval, 0)

		if key == "5":

			Sensor = "0001"
			client.publish("actions_789/", "SELECT_SENSOR" + "," + Sensor, 0)			

if __name__ == '__main__':
	main()

sys.exit(0)
