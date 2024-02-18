import paho.mqtt.client as mqttc
from paho import *
import time

from paho import mqtt

from model.CardiovascularMonitoringWearable import CardiovascularMonitoringWearable
from model.CardiovascularTelemetry import CardiovascularTelemetry
import conf.MQTT_configuration_params as Params

def on_connect(client, userdata, flags, rc):
    print(f'Connected with result code {rc}')
    publish_device_info()


def publish_telemetry_data():
    target_topic = (f'{Params.MQTT_BASIC_TOPIC}/{Params.WEARABLE_TOPIC}/{wearable_id}/'
                    f'{Params.WEARABLE_TELEMETRY_TOPIC}')

    device_payload = cardio_telemetry.to_json()
    mqtt_client.publish(target_topic, device_payload, qos = 0, retain = False)
    print(f'Telemetry data published -> Topic: {target_topic} Payload: {device_payload}')


def publish_device_info():
    target_topic = (f'{Params.MQTT_BASIC_TOPIC}/{Params.WEARABLE_TOPIC}/{wearable.uuid}/'
                    f'{Params.WEARABLE_INFO_TOPIC}')

    device_payload = wearable.to_json()
    mqtt_client.publish(target_topic, device_payload, qos = 0, retain = True)
    print(f'Wearable info published -> Topic: {target_topic} Payload: {device_payload}')


# Configurazione del client publisher MQTT.
wearable_id = f'wearable-{Params.MQTT_USERNAME}'
mqtt_client = mqttc.Client(wearable_id)
mqtt_client.on_connect = on_connect
mqtt_client.username_pw_set(Params.MQTT_USERNAME, Params.MQTT_PASSWORD)

# Dichiarazione dell'effettivo oggetto wearable.
wearable = CardiovascularMonitoringWearable(
    uuid = wearable_id,
    manufacturer = 'Dario\'s ltd',
    model = 'pro',
    owner_id = Params.MQTT_USERNAME
)

print(f'Connecting to {Params.BROKER_ADDRESS}, Port: {Params.BROKER_PORT}')
mqtt_client.connect(Params.BROKER_ADDRESS, Params.BROKER_PORT)

# Mette in funzione il client MQTT.
mqtt_client.loop_start()

# Trasmissione delle effettive misurazioni del device.
cardio_telemetry = CardiovascularTelemetry()

# Numero limite di messaggi tramessi.
message_limit = 1000
for message_id in range(message_limit):
    cardio_telemetry.update_values_randomly()
    publish_telemetry_data()
    time.sleep(3)

mqtt_client.loop_stop()

