import logging
from bluepy.btle import Peripheral, BTLEDisconnectError

_LOGGER = logging.getLogger(__name__)


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

        except BTLEDisconnectError as err:
            _LOGGER.error(f'BT connection error: {err}')
        finally:
            if self.device is not None:
                self.device.disconnect()

    def _switch_power(self, state):
        if state == 'OFF':
            self.handle.write(b'\x7e\x00\x04\x00\x00\x00\x00\x00\xef')
        else:
            self.handle.write(b'\x7e\x00\x04\x01\x00\x00\x00\x00\xef')

    def _set_light(self, new_state):
        color = new_state.get('color')
        if color is not None:
            packet = frame = b'\x7e\x00\x05\x03'
            packet += bytes([color['r']])
            packet += bytes([color['g']])
            packet += bytes([color['b']])
            packet += b'\x00\xef'
            self.handle.write(packet)

        brightness = new_state.get('brightness')
        if brightness is not None:
            packet = b'\x7e\x00\x01'
            packet += bytes([brightness])
            packet += b'\x00\x00\x00\x00\xef'
            self.handle.write(packet)

    def _get_state_handle(self):
        self.device = Peripheral(self.mac)
        services = list(self.device.getServices())

        for service in services:
            characteristics = service.getCharacteristics()
            for handle in characteristics:
                if handle.propertiesToString().find('WRITE') > 0:
                    self.handle = handle
                    return

        raise BTLEDisconnectError('failed to retrieve writable attribute')
