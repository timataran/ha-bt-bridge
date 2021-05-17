class MqttConfig:
    broker = '192.168.0.1'
    port = 1883
    username = 'username'
    password = 'password'
    topic = 'bt-bridge'


class LedConfig:
    MAC = 'be:58:c0:00:6d:fc'
    discovery_prefix = 'homeassistant'
    unique_id = 'bt_led_light'
    name = 'Bluetooth LED light'


class Config:
    MQTT = MqttConfig()
    device = LedConfig()
