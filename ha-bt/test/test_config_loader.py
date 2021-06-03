from unittest import TestCase
from config_loader import ConfigLoader


class TestConfigLoader(TestCase):

    def test_load_test_config(self):
        loader = ConfigLoader()
        config = loader.load('test/test_config.yaml')

        self.assertEqual('192.168.0.1', config.MQTT.broker)
        self.assertEqual(1883, config.MQTT.port)
        self.assertEqual('username', config.MQTT.username)
        self.assertEqual('password', config.MQTT.password)

        devices = config.devices

        expected_devices = [
            {
                "type": 'led_rgb',
                "MAC": 'be:58:c0:00:6d:fc',
                "unique_id": 'bt_led_light_one',
                "name": 'First BT LED light',
                "discovery_prefix": 'home_assistant'
            },
            {
                "type": 'led_rgb',
                "MAC": 'ba:34:d8:00:8f:bb',
                "unique_id": 'bt_led_light_two',
                "name": 'Second BT LED light',
                "discovery_prefix": 'home_assistant'
            },
            {
                "type": 'mitemp2',
                "MAC": 'a4:c1:38:15:91:10',
                "unique_id": 'mitemp_sensor_one',
                "name": 'First MiTemperature2 sensor',
                "poll_period": 180,
                "discovery_prefix": 'home_assistant',
                "read_timeout": 12
            }
        ]

        for idx in [0, 1, 2]:
            expected_config = expected_devices[idx]
            for key in expected_config.keys():
                self.assertEqual(expected_config[key], getattr(devices[idx], key))

        timer = config.timer
        self.assertEqual(2, timer.sleep_seconds)
