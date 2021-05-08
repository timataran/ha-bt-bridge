import logging
import json
import paho.mqtt.client as mqtt
from config import Config
from device.elk_bledom import LedRgb, Effect

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
_LOGGER = logging.getLogger('ha-bt')

_CONFIG = Config()


def connect_mqtt() -> mqtt:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            _LOGGER.info("Connected to MQTT Broker!")
        else:
            _LOGGER.error(f"Failed to connect, return code {rc}\n")

    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(_CONFIG.MQTT.username, _CONFIG.MQTT.password)
    mqtt_client.on_connect = on_connect
    mqtt_client.connect(_CONFIG.MQTT.broker, _CONFIG.MQTT.port)
    return mqtt_client


def send_config(client):
    topic = 'homeassistant/light/rgb_stripe_one/config'

    config = {
        "schema": "json",
        "name": "RGB stripe test",
        "command_topic": "homeassistant/light/rgb_stripe_one/set",
        "state_topic": "homeassistant/light/rgb_stripe_one/state",
        "unique_id": "rgb_stripe_one",
        "brightness": True,
        "brightness_scale": 100,
        "rgb": True,
        "effect": True,
        "effect_list": Effect.get_effect_list()
    }

    client.publish(topic, json.dumps(config), qos=1)


def subscribe(mqtt_client):
    def on_message(client, userdata, msg):
        payload = msg.payload.decode()
        _LOGGER.debug(f"Received `{payload}` from `{msg.topic}` topic")
        state = json.loads(payload)
        led = LedRgb(_CONFIG.MAC)
        led.set_state(state)
        if state.get('color') is not None:
            state['effect'] = None
        mqtt_client.publish('homeassistant/light/rgb_stripe_one/state', json.dumps(state), qos=1)

    mqtt_client.subscribe('homeassistant/light/rgb_stripe_one/set')
    mqtt_client.on_message = on_message


def run():
    client = connect_mqtt()
    send_config(client)
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    _LOGGER.info('HA-BT start')
    run()
