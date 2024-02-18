import paho.mqtt.client as mqttc
import paho.mqtt as mqtt
import paho

sub_client = mqttc.Client('test')
def on_connect(client, userdata, flags, rc):
    print(f'Connected with result {rc}')
    sub_client.subscribe('iot/test1/client1')


def on_message(client, userdata, msg):
    print(msg.payload.decode('utf-8'))

sub_client.on_connect = on_connect
sub_client.on_message = on_message

sub_client.connect('127.0.0.1', 1883)

while True:
    sub_client.loop()