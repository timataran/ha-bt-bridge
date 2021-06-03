from unittest import TestCase
from unittest.mock import Mock, patch, call
from device.mitemp2 import MiTemp2
import time


@patch('device.mitemp2.Thermometer')
class TestLedDevice(TestCase):

    def test_send_discovery_config_on_connect(self, driver_mock):
        bridge = Mock()
        device = MiTemp2(TestConfig())

        device.connect(bridge)

        calls = [
            call(
                'homeassistant/sensor/unique_id_temperature/config',
                {
                    "state_topic": "homeassistant/sensor/unique_id/state",
                    "name": "Friendly name temperature",
                    "device_class": "temperature",
                    "unit_of_measurement": "°C",
                    "value_template": "{{value_json.temperature}}"
                }
            ),
            call(
                'homeassistant/sensor/unique_id_humidity/config',
                {
                    "state_topic": "homeassistant/sensor/unique_id/state",
                    "name": "Friendly name humidity",
                    "device_class": "humidity",
                    "unit_of_measurement": "%",
                    "value_template": "{{value_json.humidity}}"
                }
            ),
            call(
                'homeassistant/sensor/unique_id_battery/config',
                {
                    "state_topic": "homeassistant/sensor/unique_id/state",
                    "name": "Friendly name battery",
                    "device_class": "battery",
                    "unit_of_measurement": "%",
                    "value_template": "{{value_json.battery}}"
                }
            ),
            call(
                'homeassistant/sensor/unique_id_voltage/config',
                {
                    "state_topic": "homeassistant/sensor/unique_id/state",
                    "name": "Friendly name voltage",
                    "device_class": "voltage",
                    "unit_of_measurement": "V",
                    "value_template": "{{value_json.voltage}}"
                }
            )
        ]

        bridge.send.assert_has_calls(calls, any_order=True)

    def test_send_status_on_connect(self, driver_mock):
        driver = driver_mock.return_value
        driver.read.return_value = {"foo": "bar"}

        bridge = Mock()
        device = MiTemp2(TestConfig())

        device.connect(bridge)

        bridge.send.assert_has_calls([call(
            "homeassistant/sensor/unique_id/state",
            {"foo": "bar"}
        )])

    @patch('device.mitemp2.schedule')
    def test_schedule_periodic_status_send_on_connect(self, schedule_mock, driver_mock):
        config = TestConfig()
        device = MiTemp2(config)

        bridge = Mock()
        device.connect(bridge)

        schedule_mock.every.assert_called_with(config.poll_period)

        every_result = schedule_mock.every.return_value
        do_method_param = every_result.seconds.do.call_args[0][0]

        bridge.reset_mock()
        bridge.send.assert_not_called()

        do_method_param()

        bridge.send.assert_called()

    def test_log_error_reading_on_lasts_too_long(self, driver_mock):

        def long_read():
            time.sleep(5)

        driver = driver_mock.return_value
        driver.read.side_effect = long_read

        bridge = Mock()
        device = MiTemp2(TestConfig())

        with self.assertLogs('device.mitemp2', level='ERROR') as log_context:
            device.connect(bridge)

        self.assertEqual(
            ["ERROR:device.mitemp2:'Timed Out'"],
            log_context.output
        )


class TestConfig:
    type = 'MiTemp2'
    MAC = 'device_mac'
    discovery_prefix = 'homeassistant'
    unique_id = 'unique_id'
    name = 'Friendly name'
    poll_period = 120
    read_timeout = 0.1
    timeout_by_signals = True
