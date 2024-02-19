import json
from typing import Callable
import paho.mqtt.client as mqtt
from model.CardiovascularMonitoringWearable import CardiovascularMonitoringWearable
import conf.MQTT_configuration_params as Params


def on_connect(client, userdata, flags, rc):
    print(f'Connected with result code {rc}')

    device_info_topic = (f'{Params.MQTT_BASIC_TOPIC}/{Params.WEARABLE_TOPIC}/+/'
                         f'{Params.WEARABLE_INFO_TOPIC}')

    client.subscribe(device_info_topic)
    print(f'Subscribed to: {device_info_topic}')

    device_telemetry_topic = (f'{Params.MQTT_BASIC_TOPIC}/{Params.WEARABLE_TOPIC}/+/'
                              f'{Params.WEARABLE_TELEMETRY_TOPIC}')

    client.subscribe(device_telemetry_topic)
    print(f'Subscribed to: {device_telemetry_topic}')

    device_status_topic = (f'{Params.MQTT_BASIC_TOPIC}/{Params.WEARABLE_TOPIC}/+/'
                              f'{Params.WEARABLE_STATUS_TOPIC}')

    client.subscribe(device_status_topic)
    print(f'Subscribed to: {device_status_topic}')


def on_message(client, userdata, message):
    message_payload = str(message.payload.decode('utf-8'))
    print(f'<<{message.topic}>> -> {message_payload}')

    splitted_topic = message.topic.split('/')
    data_type = splitted_topic[-1]
    device = splitted_topic[-2]

    with open(f'messages-{device}.log', 'a', encoding = 'utf-8') as file:
        file.write(f'{message_payload}\n')
        if data_type == 'status':
            dict_payload = json.loads(message_payload)
            if dict_payload['anomaly']:
                file.write(f'###### ANOMALY ######\n')


def data_collection():
    data_collector_mqtt_client = mqtt.Client('datamanager')
    data_collector_mqtt_client.on_message = on_message
    data_collector_mqtt_client.on_connect = on_connect
    data_collector_mqtt_client.username_pw_set(Params.MQTT_USERNAME, Params.MQTT_PASSWORD)
    data_collector_mqtt_client.connect(Params.BROKER_ADDRESS, Params.BROKER_PORT)
    data_collector_mqtt_client.loop_forever()


if __name__ == '__main__':
    data_collection()