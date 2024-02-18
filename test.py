import time

import paho.mqtt.client as mqttc

client = mqttc.Client('test1')

client.connect('127.0.0.1', 1883)

i = 0
while True:
    i += 1
    client.publish('iot/test1/client1', str(i), retain = True, qos = 0)
    print(f'message sent: {i}')
    time.sleep(2)