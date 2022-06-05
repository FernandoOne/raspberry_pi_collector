import sys
import time

import paho.mqtt.client

def outputToFile(data):
    with open('data_received_through_mqtt.txt', 'a') as f:
        f.write(data+"\n")

def on_connect(client, userdata, flags, rc):
	print('connected (%s)' % client._client_id)
	client.subscribe("intel_agri/sensor_data/#", qos=2)
	#client.subscribe(topic='data/', qos=2)

def on_message(client, userdata, message):
    print(message.payload)
    #outputToFile(str(message.payload))

def main():
	client = paho.mqtt.client.Client(client_id='server', clean_session=False)
	client.tls_set(tls_version=paho.mqtt.client.ssl.PROTOCOL_TLS)
	client.username_pw_set("AgriIntel", "Qwerty135")
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(host='b94fa7cf0c0f4fcd91c97460db5c0564.s2.eu.hivemq.cloud', port=8883)
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
			
			setReportIntervalAction="{\"Action_name\": \"SET_REPORT_INTERVAL\", \"Address\": \"0001\", \"Report_interval\": \"00006000\"}"

			print("Enter interval:")
			#Interval = input()
			client.publish("intel_agri/actions", setReportIntervalAction, 0)

		if key == "5":

			Sensor = "0001"
			client.publish("intel_agri/actions", "SELECT_SENSOR" + "," + Sensor, 0)			

if __name__ == '__main__':
	main()

sys.exit(0)
