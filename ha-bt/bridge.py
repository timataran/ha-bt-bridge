import logging
import json
import paho.mqtt.client as mqtt

_LOGGER = logging.getLogger(__name__)


class Bridge:
    def __init__(self, config):
        self.config = config
        self.mqtt_client = self._connect_mqtt(config)
        self.listeners = {}

    def add_listener(self, topic, method):
        self.mqtt_client.subscribe(topic)
        self.listeners[topic] = method

    def send(self, topic, message):
        self.mqtt_client.publish(topic, json.dumps(message), qos=1)

    def start(self):
        self.mqtt_client.loop_forever()

    def _on_message(self, client, userdata, message):
        topic = message.topic
        payload = message.payload.decode()
        _LOGGER.debug(f"Received `{payload}` from `{topic}` topic")
        topic_listener = self.listeners.get(topic)
        if topic_listener is not None:
            topic_listener(json.loads(payload))

    @staticmethod
    def _on_connect(client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            _LOGGER.info("Connected to MQTT Broker!")
        else:
            raise MqttConnectError(f"Failed to connect, return code {reason_code}\n")

    def _connect_mqtt(self, config):
        try:
            mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
            mqtt_client.username_pw_set(config.username, config.password)
            mqtt_client.on_connect = self._on_connect
            mqtt_client.on_message = self._on_message

            connect_attributes = {"keepalive": config.keepalive} if hasattr(config, 'keepalive') else {}

            mqtt_client.connect(config.broker, config.port, **connect_attributes)
            return mqtt_client
        except Exception as err:
            raise MqttConnectError(err)


class MqttConnectError(Exception):
    pass

