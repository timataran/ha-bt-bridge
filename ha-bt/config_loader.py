import yaml


class ConfigLoader:
    def __init__(self):
        self.yaml_content = None

    def load(self, filename):
        if filename is None:
            filename = './config.yaml'

        with open(filename) as file:
            self.yaml_content = yaml.safe_load(file)

        mqtt_config = self._build_mqtt_config()
        devices = self._build_devices_config()

        config = Config()
        setattr(config, 'MQTT', mqtt_config)
        setattr(config, 'devices', devices)

        return config

    def _build_mqtt_config(self):
        config = Config()
        config_data = self.yaml_content.get('mqtt')
        setattr(config, 'broker', config_data.get('broker'))
        setattr(config, 'port', config_data.get('port'))
        setattr(config, 'username', config_data.get('username'))
        setattr(config, 'password', config_data.get('password'))
        setattr(config, 'discovery_prefix', config_data.get('discovery_prefix'))
        return config

    def _build_devices_config(self):
        mqtt_data = self.yaml_content.get('mqtt')
        device_data = self.yaml_content.get('device')
        devices = []

        for device in device_data:
            device_config = Config()
            setattr(device_config, 'discovery_prefix', mqtt_data.get('discovery_prefix'))
            setattr(device_config, 'type', device.get('type'))
            setattr(device_config, 'MAC', device.get('MAC'))
            setattr(device_config, 'unique_id', device.get('unique_id'))
            setattr(device_config, 'name', device.get('name'))

            devices.append(device_config)

        return devices


class Config:
    pass
