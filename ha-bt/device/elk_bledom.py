import logging
import bluepy.btle

_LOGGER = logging.getLogger(__name__)

ZERO = b'\x00'


class LedRgb:
    def __init__(self, mac):
        self.mac = mac
        self.device = None
        self.handle = None

    def set_state(self, new_state):
        try:
            self._get_state_handle()

            if list(new_state.keys()) == ['state']:
                self._switch_power(new_state['state'])
            else:
                self._set_light(new_state)

        except bluepy.btle.BTLEDisconnectError as err:
            _LOGGER.error(f'BT connection error: {err}')
        finally:
            if self.device is not None:
                self.device.disconnect()

    def _switch_power(self, state):
        if state == 'OFF':
            self._send_packet(b'\x04', b'\x00')
        else:
            self._send_packet(b'\x04', b'\x01')

    def _set_light(self, new_state):
        color = new_state.get('color')
        if color is not None:
            self._send_packet(
                b'\x05',
                b'\x03',
                bytes([color['r']]),
                bytes([color['g']]),
                bytes([color['b']]),
            )

        brightness = new_state.get('brightness')
        if brightness is not None:
            self._send_packet(b'\x01', bytes([brightness]))

    def _get_state_handle(self):
        self.device = bluepy.btle.Peripheral(self.mac)
        characteristics = self.device.getCharacteristics()

        for handle in characteristics:
            if handle.propertiesToString().find('WRITE') > 0:
                self.handle = handle
                return

        raise bluepy.btle.BTLEDisconnectError('failed to retrieve writable attribute')

    def _send_packet(self, command, sub_command, arg_1=ZERO, arg_2=ZERO, arg_3=ZERO):
        packet = b'\x7e\x00' + command + sub_command + arg_1 + arg_2 + arg_3 + b'\x00\xef'
        self.handle.write(packet)
