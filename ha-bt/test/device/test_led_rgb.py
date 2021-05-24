from unittest import TestCase
from unittest.mock import Mock, patch
from device.led_rgb import LedRgb
import test.utils as utils


class TestLedDevice(TestCase):

    def test_send_discovery_config_on_connect(self):
        bridge = Mock()
        device = LedRgb(TestConfig())

        device.connect(bridge)

        bridge.send.assert_called_with(
            'homeassistant/light/unique_id/config',
            {
                "schema": "json",
                "name": "Friendly name",
                "command_topic": 'homeassistant/light/unique_id/set',
                "state_topic": 'homeassistant/light/unique_id/state',
                "unique_id": "unique_id",
                "brightness": True,
                "brightness_scale": 100,
                "rgb": True,
                "effect": True,
                "effect_list": utils.ELK_BLEDOM_EFFECT_LIST
            }
        )

    def test_call_bridge_add_listener_on_connect(self):
        bridge = Mock()
        device = LedRgb(TestConfig())

        device.connect(bridge)

        bridge.add_listener.assert_called_with(
            'homeassistant/light/unique_id/set',
            device.on_state_update_received
        )

    def test_log_info_on_connect(self):
        bridge = Mock()
        device = LedRgb(TestConfig())

        with self.assertLogs('device.base', 'INFO') as log_context:
            device.connect(bridge)

        self.assertEqual(
            ["INFO:device.base:LedRgb device with MAC device_mac connected to bridge"],
            log_context.output
        )

    @patch('device.led_rgb.Led')
    def test_build_driver_with_device_MAC(self, driver_mock):
        LedRgb(TestConfig)

        driver_mock.assert_called_with(TestConfig.MAC)

    @patch('device.led_rgb.Led')
    def test_call_driver_set_state_on_state_update(self, driver_mock):
        device = LedRgb(TestConfig())
        device.connect(Mock())

        device.on_state_update_received({"foo": "new_state"})

        driver = driver_mock.return_value

        driver.set_state.assert_called_with({"foo": "new_state"})

    @patch('device.led_rgb.Led')
    def test_send_back_applied_state(self, _):
        bridge = Mock()
        device = LedRgb(TestConfig())
        device.connect(bridge)

        device.on_state_update_received(
            {
                "state": "ON",
                "color": {"r": 255, "g": 0, "b": 63},
                "effect": "CROSSFADE_CYAN"
            }
        )

        bridge.send.assert_called_with(
            device.state_topic,
            {
                "state": "ON",
                "color": {"r": 255, "g": 0, "b": 63},
                "effect": None
            }
        )


class TestConfig:
    type = 'LedRgb'
    MAC = 'device_mac'
    discovery_prefix = 'homeassistant'
    unique_id = 'unique_id'
    name = 'Friendly name'
