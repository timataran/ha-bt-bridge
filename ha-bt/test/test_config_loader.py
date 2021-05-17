from unittest import TestCase
from config_loader import ConfigLoader


class TestConfigLoader(TestCase):

    def test_load_test_config(self):
        loader = ConfigLoader()
        config = loader.load('test/config.yaml')

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
            }
        ]

        for idx in [0, 1]:
            self.assertEqual(expected_devices[idx]['type'], devices[idx].type)
            self.assertEqual(expected_devices[idx]['MAC'], devices[idx].MAC)
            self.assertEqual(expected_devices[idx]['unique_id'], devices[idx].unique_id)
            self.assertEqual(expected_devices[idx]['name'], devices[idx].name)
            self.assertEqual(expected_devices[idx]['discovery_prefix'], devices[idx].discovery_prefix)
