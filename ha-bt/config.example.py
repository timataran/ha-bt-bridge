class MqttConfig:
    broker = '192.168.0.1'
    port = 1883
    username = 'username'
    password = 'password'
    topic = 'bt-bridge'


class Config:
    MQTT = MqttConfig()
    MAC = 'aa:bb:22:33:44:55'
