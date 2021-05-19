from unittest import TestCase
from unittest.mock import patch
from device.mitemp.driver import Thermometer
from device.error import BTConnectError


# noinspection PyBroadException
@patch('device.mitemp.driver.Connection')
class TestConnection(TestCase):

    def test_build_connection_with_mac(self, connection_mock):
        Thermometer('mac-address')

        connection_mock.assert_called_with('mac-address')

    def test_decode_received_data(self, connection_mock):
        connection = connection_mock.return_value
        connection.read.return_value = b'\xa3\t:\xd9\x0b'

        driver = Thermometer('mac_address')

        result = driver.read()

        self.assertEqual(
            {
                "temperature": 24.7,
                "humidity": 58,
                "voltage": 3.033,
                "battery_level": 93
            },
            result
        )

    def test_write_log_on_error(self, connection_mock):
        connection = connection_mock.return_value
        connection.read.side_effect = BTConnectError('Test error message')

        driver = Thermometer('mac_address')

        with self.assertLogs('device.mitemp.driver', level='ERROR') as log_context:
            driver.read()

        self.assertEqual(
            ['ERROR:device.mitemp.driver:BT connection error: Test error message'],
            log_context.output
        )
