from datetime import datetime
import json

import paho.mqtt.client as mqttc
from paho import *
import time
from model.StatusTelemetry import StatusTelemetry

from paho import mqtt

from model.CardiovascularMonitoringWearable import CardiovascularMonitoringWearable
from model.CardiovascularTelemetry import CardiovascularTelemetry
import conf.MQTT_configuration_params as Params

def on_connect(client, userdata, flags, rc):
    print(f'Connected with result code {rc}')


def add_timestamp(payload: str) -> str:
    # Get date and time
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

    # Adds timestamp
    dict_payload = json.loads(payload)
    dict_payload.update({'timestamp': date_time})

    payload_with_timestamp = json.dumps(dict_payload)
    return payload_with_timestamp

class Emulator:
    mqtt_client: mqttc.Client
    wearable: CardiovascularMonitoringWearable
    cardio_telemetry: CardiovascularTelemetry
    status_telemetry: StatusTelemetry

    def __init__(self, wearable: CardiovascularMonitoringWearable):
        self.wearable = wearable
        self.cardio_telemetry = CardiovascularTelemetry()
        self.status_telemetry = StatusTelemetry()

        # Configurazione del client publisher MQTT.
        self.mqtt_client = mqttc.Client(self.wearable.uuid)
        self.mqtt_client.on_connect = on_connect
        self.mqtt_client.username_pw_set(Params.MQTT_USERNAME, Params.MQTT_PASSWORD)

        print(f'Connecting to {Params.BROKER_ADDRESS}, Port: {Params.BROKER_PORT}')
        self.mqtt_client.connect(Params.BROKER_ADDRESS, Params.BROKER_PORT)

    def publish_telemetry_data(self):
        target_topic = (f'{Params.MQTT_BASIC_TOPIC}/{Params.WEARABLE_TOPIC}/{self.wearable.uuid}/'
                        f'{Params.WEARABLE_TELEMETRY_TOPIC}')

        device_payload = self.cardio_telemetry.to_json()
        device_payload_with_timestamp = add_timestamp(device_payload)

        self.mqtt_client.publish(target_topic, device_payload_with_timestamp, qos = 0, retain = False)
        print(f'Telemetry data published -> Topic: {target_topic} Payload: {device_payload}')


    def publish_device_info(self):
        target_topic = (f'{Params.MQTT_BASIC_TOPIC}/{Params.WEARABLE_TOPIC}/{self.wearable.uuid}/'
                        f'{Params.WEARABLE_INFO_TOPIC}')

        device_payload = self.wearable.to_json()
        payload_with_timestamp = add_timestamp(device_payload)

        self.mqtt_client.publish(target_topic, payload_with_timestamp, qos = 0, retain = True)
        print(f'Wearable info published -> Topic: {target_topic} Payload: {device_payload}')

    def publish_status_data(self):
        target_topic = (f'{Params.MQTT_BASIC_TOPIC}/{Params.WEARABLE_TOPIC}/{self.wearable.uuid}/'
                        f'{Params.WEARABLE_STATUS_TOPIC}')

        device_payload = self.status_telemetry.to_json()
        payload_with_timestamp = add_timestamp(device_payload)

        self.mqtt_client.publish(target_topic, payload_with_timestamp, qos = 2, retain = True)
        print(f'Status data published -> Topic: {target_topic} Payload: {device_payload}')

    def start(self):
        self.mqtt_client.loop()

    def stop(self):
        self.mqtt_client.loop_stop()

    def detect_anomalies(self) -> bool:
        if self.cardio_telemetry.heart_rate < 65 or self.cardio_telemetry.heart_rate > 110:
            return True

        if self.cardio_telemetry.oxygen_saturation < 0.9:
            return True

        return False

def main():

    # Dichiarazione dell'effettivo oggetto wearable.
    wearable_dario = CardiovascularMonitoringWearable(
        uuid = 'wearable-dario',
        manufacturer = 'company ltd',
        model = 'pro',
        owner_id = 'dario'
    )

    wearable_luca = CardiovascularMonitoringWearable(
        uuid = 'wearable-luca',
        manufacturer = 'company ltd',
        model = 'basic',
        owner_id = 'luca'
    )

    wearables = [wearable_dario, wearable_luca]

    wearables_emus = []
    for wearable in wearables:
        wearables_emus.append(Emulator(wearable))

    for emu in wearables_emus:
        emu.publish_device_info()
        emu.start()

    # Numero limite di messaggi tramessi.
    message_limit = 1000
    for message_id in range(message_limit):
        for emu in wearables_emus:
            emu.cardio_telemetry.update_values_randomly()
            emu.status_telemetry.simulate_battery_discharge()

            if emu.detect_anomalies():
                emu.status_telemetry.anomaly = True
            else:
                emu.status_telemetry.anomaly = False

            if not emu.status_telemetry.battery_level < 0:
                emu.publish_telemetry_data()
                emu.publish_status_data()

        time.sleep(3)
        # in una implementazione reale di questa simulazione è possibile determinare
        # singolarmente la frequenza di trasmissione delle misurazioni eseguite dai vari
        # dispositivi wearable. A scopi simulativi sarebbe possbile ottenere un risultato simile
        # utilizzando un approccio multithrading.

    for emu in wearables_emus:
        emu.stop()


if __name__ == '__main__':
    main()
