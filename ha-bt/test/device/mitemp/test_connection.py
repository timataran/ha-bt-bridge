from unittest import TestCase
from unittest.mock import patch
from device.mitemp.connection import Connection
from device.error import BTConnectError
from bluepy.btle import BTLEDisconnectError


# noinspection PyBroadException
@patch('device.mitemp.connection.Peripheral')
class TestConnection(TestCase):

    def test_get_device_by_mac(self, peripheral_mock):
        connection = Connection('mac_value')
        try:
            connection.read()
        except:
            pass

        peripheral_mock.ssert_called_with('mac_value')

    def test_throw_custom_error_on_no_data_received(self, _):
        connection = Connection('mac_value')

        with self.assertRaises(BTConnectError) as error_context:
            connection.read()
        error = error_context.exception

        self.assertEqual('Failed to retrieve sensor data', str(error))

    def test_throw_custom_error_on_connection_error(self, peripheral_mock):
        peripheral_mock.side_effect = BTLEDisconnectError('Failed to connect to peripheral')

        connection = Connection('mac_value')

        with self.assertRaises(BTConnectError) as error_context:
            connection.read()
        error = error_context.exception

        self.assertEqual('Failed to connect to peripheral', str(error))
