import sys
import time

import paho.mqtt.client

def outputToFile(data):
    with open('data_received_through_mqtt.txt', 'a') as f:
        f.write(data+"\n")

def on_connect(client, userdata, flags, rc):
	print('connected (%s)' % client._client_id)
	client.subscribe(topic='actions/', qos=2)

def on_message(client, userdata, message):
    print(message.payload)
    #outputToFile(str(message.payload))

def main():
	client = paho.mqtt.client.Client(client_id='RaspberryPi', clean_session=True)
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(host='127.0.0.1', port=1883)
	client.loop_forever()

if __name__ == '__main__':
	main()

sys.exit(0)
