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
	#client.loop_forever()
	
	q=0
	while 1:
		client.publish("actions/", "Dataso", 0)
		print("Dataso" + str(q))
		q=q+1
		time.sleep(5)

if __name__ == '__main__':
	main()

sys.exit(0)
