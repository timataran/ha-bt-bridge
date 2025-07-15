from unittest import TestCase
from unittest.mock import patch
from device.mitemp.connection import Connection
from device.error import BTConnectError
from bluepy.btle import BTLEDisconnectError

_V1_RESPONSE = '1.0.0_0109'.encode('utf-8')
_V2_RESPONSE = '2.1.1_0159'.encode('utf-8')
_V3_RESPONSE = '3.3.3_3333'.encode('utf-8')


# noinspection PyBroadException
@patch('device.mitemp.connection.Peripheral')
class TestConnection(TestCase):

    def test_get_device_by_mac(self, peripheral_mock):
        connection = Connection('mac_value')
        try:
            connection.read()
        except:
            pass

        peripheral_mock.assert_called_with('mac_value')

    def test_throw_custom_error_on_unknown_device_version(self, peripheral_mock):
        peripheral_mock.return_value.readCharacteristic.return_value = _V3_RESPONSE
        connection = Connection('mac_value')

        with self.assertRaises(BTConnectError) as error_context:
            connection.read()
        error = error_context.exception

        self.assertEqual('Unknown device version: 3.3.3_3333', str(error))

    def test_throw_custom_error_on_no_data_received(self, peripheral_mock):
        peripheral_mock.return_value.readCharacteristic.return_value = _V1_RESPONSE
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
