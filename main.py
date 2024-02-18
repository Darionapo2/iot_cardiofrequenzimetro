from conf import MQTT_configuration_params as Params
import paho.mqtt.client as mqtt

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

def main():
    wearable_id = f'wearable-{Params.MQTT_USERNAME}'
    message_limit = 1000

    mqtt_client = mqtt.Client(wearable_id)
    mqtt_client.on_message = on_message
    mqtt_client.on_connect = on_connect

    mqtt_client.username_pw_set(Params.MQTT_USERNAME, Params.MQTT_PASSWORD)

    print(f'Connecting to {Params.BROKER_ADDRESS}, port: {Params.BROKER_PORT}')
    mqtt_client.connect(Params.BROKER_ADDRESS, Params.BROKER_PORT)

    mqtt_client.loop_forever()

if __name__ == '__main__':
    main()