import sys
import time

import paho.mqtt.client

def outputToFile(data):
    with open('data_received_through_mqtt.txt', 'a') as f:
        f.write(data+"\n")

def on_connect(client, userdata, flags, rc):
	print('connected (%s)' % client._client_id)
	client.subscribe(topic='intel_agri/sensor_data', qos=2)

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

			client.publish("intel_agri/actions", "{\"Action_name\": \"FORM_NETWORK\"}", 0)

		if key == "2":

			client.publish("intel_agri/actions", "{\"Action_name\": \"OPEN_NETWORK\"}", 0)

		if key == "3":

			client.publish("intel_agri/actions", "{\"Action_name\": \"CLOSE_NETWORK\"}", 0)

		if key == "4":
		
			setReportIntervalAction="{\"Action_name\": \"SELECT_SENSOR_AND_SET_REPORT_INTERVAL\", \"Address\": \"0001\", \"Parameter\": \"00010000\"}"
			client.publish("intel_agri/actions", setReportIntervalAction, 0)	

		if key == "5":

			selectSensor = "{\"Action_name\": \"SELECT_SENSOR\", \"Parameter\": \"0001\"}"
			client.publish("intel_agri/actions", selectSensor, 0)	

		if key == "6":
	
			setReportIntervalAction="{\"Action_name\": \"SET_REPORT_INTERVAL\", \"Parameter\": \"00003000\"}"
			client.publish("intel_agri/actions", setReportIntervalAction, 0)	

		if key == "7":

			setOpenValve="{\"Action_name\": \"SELECT_SENSOR_AND_OPEN_VALVE\", \"Address\": \"0001\"}"
			client.publish("intel_agri/actions", setOpenValve, 0)	

		if key == "8":

			setCloseValve="{\"Action_name\": \"SELECT_SENSOR_AND_CLOSE_VALVE\", \"Address\": \"0001\"}"
			client.publish("intel_agri/actions", setCloseValve, 0)	

if __name__ == '__main__':
	main()

sys.exit(0)
