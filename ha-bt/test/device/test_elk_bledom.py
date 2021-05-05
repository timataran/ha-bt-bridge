from unittest import TestCase
from unittest.mock import Mock, patch
from device.elk_bledom import LedRgb


@patch("device.elk_bledom.bluepy.btle")
class TestCommands(TestCase):

    def test_send_switch_on_packet(self, btle_mock):
        attribute = self._build_characteristic_mock()
        device_mock = Mock()
        device_mock.getCharacteristics.return_value = [attribute]

        btle_mock.Peripheral.return_value = device_mock

        led = LedRgb('mac value')
        led.set_state({'state': 'ON'})

        attribute.write.assert_called_with(b'\x7e\x00\x04\x01\x00\x00\x00\x00\xef')

    def test_send_switch_off_packet(self, btle_mock):
        attribute = self._build_characteristic_mock()
        device_mock = Mock()
        device_mock.getCharacteristics.return_value = [attribute]

        btle_mock.Peripheral.return_value = device_mock

        led = LedRgb('mac value')
        led.set_state({'state': 'OFF'})

        attribute.write.assert_called_with(b'\x7e\x00\x04\x00\x00\x00\x00\x00\xef')

    def test_send_color_change_packet(self, btle_mock):
        attribute = self._build_characteristic_mock()
        device_mock = Mock()
        device_mock.getCharacteristics.return_value = [attribute]

        btle_mock.Peripheral.return_value = device_mock

        led = LedRgb('mac value')
        led.set_state({'state': 'ON', 'color': {'r': 5, 'g': 255, 'b': 7}})

        attribute.write.assert_called_with(b'\x7e\x00\x05\x03\x05\xff\x07\x00\xef')

    def test_send_brightness_change_packet(self, btle_mock):
        attribute = self._build_characteristic_mock()
        device_mock = Mock()
        device_mock.getCharacteristics.return_value = [attribute]

        btle_mock.Peripheral.return_value = device_mock

        led = LedRgb('mac value')
        led.set_state({'state': 'ON', 'brightness': 50})

        attribute.write.assert_called_with(b'\x7e\x00\x01\x32\x00\x00\x00\x00\xef')

    @staticmethod
    def _build_characteristic_mock():
        attribute = Mock()
        attribute.propertiesToString.return_value = 'READ WRITE NO RESPONSE'
        return attribute

