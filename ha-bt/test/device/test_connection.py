from unittest import TestCase
from unittest.mock import Mock, patch
from device.connection import Connection, BTConnectError
from bluepy.btle import BTLEDisconnectError


@patch("device.connection.bluepy.btle")
class TestConnection(TestCase):

    def test_get_device_by_mac(self, btle_mock):
        btle_mock.Peripheral.return_value = self._build_peripheral_mock()
        connection = Connection('mac_value')
        connection.get_handle()
        btle_mock.Peripheral.assert_called_with('mac_value')

    def test_poll_device_only_once(self, btle_mock):
        device = self._build_peripheral_mock()
        btle_mock.Peripheral.return_value = device

        connection = Connection('mac_value')

        connection.get_handle()
        connection.get_handle()

        btle_mock.Peripheral.assert_called_once()
        device.getCharacteristics.assert_called_once()

        btle_mock.Peripheral.assert_called_with('mac_value')

    def test_return_writable_characteristic(self, btle_mock):
        chr_notify = self._build_characteristic_mock('NOTIFY')
        chr_write = self._build_characteristic_mock('WRITE')
        btle_mock.Peripheral.return_value = self._build_peripheral_mock([chr_notify, chr_write])
        connection = Connection('mac')
        handle = connection.get_handle()
        self.assertEqual(handle, chr_write)

    def test_throw_on_writable_characteristic_not_found(self, btle_mock):
        connection = Connection('mac_value')
        characteristic = self._build_characteristic_mock('NOTIFY')
        btle_mock.Peripheral.return_value = self._build_peripheral_mock([characteristic])
        self.assertRaises(BTConnectError, connection.get_handle)

    def test_throw_on_connection_error(self, btle_mock):

        def throw_btle_error(*args):
            raise BTLEDisconnectError('some_error')

        connection = Connection('mac_value')
        btle_mock.Peripheral.side_effect = throw_btle_error
        self.assertRaises(BTConnectError, connection.get_handle)

    def test_not_throw_on_disconnect_not_connected(self, btle_mock):
        connection = Connection('mac_value')
        try:
            connection.disconnect()
        except Exception as err:
            self.fail(f'Exception was raised: {err}')

    def test_call_device_disconnect(self, btle_mock):
        device = self._build_peripheral_mock()
        btle_mock.Peripheral.return_value = device

        connection = Connection('mac')
        connection.get_handle()
        connection.disconnect()

        device.disconnect.assert_called()

    def test_set_device_handle_none_on_disconnect(self, btle_mock):
        device = self._build_peripheral_mock()
        btle_mock.Peripheral.return_value = device

        connection = Connection('mac')
        connection.get_handle()
        connection.disconnect()

        self.assertIsNone(connection.handle)
        self.assertIsNone(connection.device)

    def _build_peripheral_mock(self, characteristics=None):
        if characteristics is None:
            characteristics = [self._build_characteristic_mock()]
        peripheral = Mock()
        peripheral.getCharacteristics.return_value = characteristics
        return peripheral

    @staticmethod
    def _build_characteristic_mock(properties_string=None):
        if properties_string is None:
            properties_string = 'READ WRITE NO RESPONSE'
        attribute = Mock()
        attribute.propertiesToString.return_value = properties_string
        return attribute
