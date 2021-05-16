from unittest import TestCase
from unittest.mock import Mock, patch
from device.led.driver import Led, Effect
from device.led.connection import BTConnectError
import test.utils as utils


@patch("device.led.driver.Connection")
class TestCommands(TestCase):
    def setUp(self):
        self.handle = Mock()
        connection = Mock()
        connection.get_handle.return_value = self.handle

        self.connection = connection

    def test_send_switch_on_packet(self, connection_mock):
        connection_mock.return_value = self.connection

        led = Led('mac value')
        led.set_state({'state': 'ON'})

        self.handle.write.assert_called_with(b'\x7e\x00\x04\x01\x00\x00\x00\x00\xef')

    def test_send_switch_off_packet(self, connection_mock):
        connection_mock.return_value = self.connection

        led = Led('mac value')
        led.set_state({'state': 'OFF'})

        self.handle.write.assert_called_with(b'\x7e\x00\x04\x00\x00\x00\x00\x00\xef')

    def test_send_color_change_packet(self, connection_mock):
        connection_mock.return_value = self.connection

        led = Led('mac value')
        led.set_state({'state': 'ON', 'color': {'r': 5, 'g': 255, 'b': 7}})

        self.handle.write.assert_called_with(b'\x7e\x00\x05\x03\x05\xff\x07\x00\xef')

    def test_send_brightness_change_packet(self, connection_mock):
        connection_mock.return_value = self.connection

        led = Led('mac value')
        led.set_state({'state': 'ON', 'brightness': 50})

        self.handle.write.assert_called_with(b'\x7e\x00\x01\x32\x00\x00\x00\x00\xef')

    def test_send_effect_change_packet(self, connection_mock):
        connection_mock.return_value = self.connection

        led = Led('mac value')
        led.set_state({'state': 'ON', 'effect': 'CROSSFADE_WHITE'})

        self.handle.write.assert_called_with(b'\x7e\x00\x03\x91\x03\x00\x00\x00\xef')

    def test_call_disconnect_on_packet_sent(self, connection_mock):
        connection_mock.return_value = self.connection

        led = Led('mac value')
        led.set_state({'state': 'ON'})

        self.connection.disconnect.assert_called_once()

    def test_log_error_on_connection_error(self, connection_mock):
        def throw_error():
            raise BTConnectError('Test error')

        connection_mock.return_value = self.connection
        self.connection.get_handle.side_effect = throw_error

        with self.assertLogs('device.led.driver', level='DEBUG') as cm:
            led = Led('mac value')
            led.set_state({'state': 'ON'})

        self.assertEqual(
            ['ERROR:device.led.driver:BT connection error: Test error'],
            cm.output
        )

    def test_effect_list(self, _):
        self.assertListEqual(
            utils.ELK_BLEDOM_EFFECT_LIST,
            Effect.get_effect_list()
        )
