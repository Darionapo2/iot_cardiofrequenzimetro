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


def on_message(client, userdata, message):
    message_payload = str(message.payload.decode('utf-8'))
    print(f'Received IoT Message: Topic: {message.topic}, Payload: {message_payload}')

class DataCollectorManager:

    log_file: str
    devices: list[CardiovascularMonitoringWearable]
    on_connect_handler: Callable
    on_message_handler: Callable

    client_mqtt: mqtt.Client

    def __init__(self, log_file: str,
                 on_connect_handler: Callable,
                 on_message_handler: Callable) -> None:

        self.log_file = log_file
        self.on_connect_handler = on_connect_handler
        self.on_message_handler = on_message_handler

        self.client_mqtt = mqtt.Client(f'datamanager-{Params.MQTT_USERNAME}')
        self.mqtt_authenticate(Params.MQTT_USERNAME, Params.MQTT_PASSWORD)

        self.mqtt_connect(Params.BROKER_ADDRESS, Params.BROKER_PORT)

    def mqtt_authenticate(self, username: str, password: str) -> None:
        self.client_mqtt.username_pw_set(username, password)

    def mqtt_connect(self, broker_address: str, broker_port: int) -> None:
        print(f'Connecting to {broker_address}, port: {broker_port}')
        self.client_mqtt.connect(broker_address, broker_port)

    def mqtt_start(self):
        self.client_mqtt.loop_forever()

    def collect(self, record: str) -> bool:
        try:
            with open(self.log_file, 'a', encoding = 'utf-8') as file:
                file.write(record)
        except FileNotFoundError:
            return False
        return True

    def add_device(self, device: CardiovascularMonitoringWearable):
        self.devices.append(device)