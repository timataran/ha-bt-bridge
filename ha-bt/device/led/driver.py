import logging
from device.led.connection import Connection, BTConnectError

_LOGGER = logging.getLogger(__name__)

ZERO = b'\x00'


class Led:
    def __init__(self, mac):
        self.connection = Connection(mac)

    def set_state(self, new_state):
        try:
            if list(new_state.keys()) == ['state']:
                self._switch_power(new_state['state'])
            else:
                self._set_light(new_state)
        finally:
            self.connection.disconnect()

    def _switch_power(self, state):
        if state == 'OFF':
            self._send_packet(Power.COMMAND, Power.OFF)
        else:
            self._send_packet(Power.COMMAND, Power.ON)

    def _set_light(self, new_state):
        color = new_state.get('color')
        if color is not None:
            self._send_packet(
                Color.COMMAND,
                Color.SUB_COMMAND,
                bytes([color['r']]),
                bytes([color['g']]),
                bytes([color['b']]),
            )

        brightness = new_state.get('brightness')
        if brightness is not None:
            self._send_packet(Brightness.COMMAND, bytes([brightness]))

        effect_name = new_state.get('effect')
        if effect_name is not None:
            self._send_packet(Effect.COMMAND, Effect.get_code(effect_name), Effect.COMMAND)

    def _send_packet(self, command, sub_command, arg_1=ZERO, arg_2=ZERO, arg_3=ZERO):
        packet = b'\x7e\x00' + command + sub_command + arg_1 + arg_2 + arg_3 + b'\x00\xef'
        self._send_packet_with_retry(packet)

    def _send_packet_with_retry(self, packet):
        send_attempt = 0
        while True:
            try:
                send_attempt += 1

                handle = self.connection.get_handle()
                handle.write(packet)
            except BTConnectError as err:
                _LOGGER.error(f'Command send attempt {send_attempt} failed with error: {err}')
                if send_attempt < 3:
                    continue
            break


class Power:
    COMMAND = b'\x04'
    ON = b'\x01'
    OFF = b'\x00'


class Brightness:
    COMMAND = b'\x01'


class Color:
    COMMAND = b'\x05'
    SUB_COMMAND = b'\x03'


class Effect:
    COMMAND = b'\x03'

    EFFECT_LIST = {
        'RED': b'\x80',
        'BLUE': b'\x81',
        'GREEN': b'\x82',
        'CYAN': b'\x83',
        'YELLOW': b'\x84',
        'MAGENTA': b'\x85',
        'WHITE': b'\x86',
        'JUMP_RED_GREEN_BLUE': b'\x87',
        'JUMP_RED_GREEN_BLUE_YELLOW_CYAN_MAGENTA_WHITE': b'\x88',
        'CROSSFADE_RED': b'\x8B',
        'CROSSFADE_GREEN': b'\x8C',
        'CROSSFADE_BLUE': b'\x8D',
        'CROSSFADE_YELLOW': b'\x8E',
        'CROSSFADE_CYAN': b'\x8F',
        'CROSSFADE_MAGENTA': b'\x90',
        'CROSSFADE_WHITE': b'\x91',
        'CROSSFADE_RED_GREEN': b'\x92',
        'CROSSFADE_RED_BLUE': b'\x93',
        'CROSSFADE_GREEN_BLUE': b'\x94',
        'CROSSFADE_RED_GREEN_BLUE': b'\x89',
        'CROSSFADE_RED_GREEN_BLUE_YELLOW_CYAN_MAGENTA_WHITE': b'\x8A',
        'BLINK_RED': b'\x96',
        'BLINK_GREEN': b'\x97',
        'BLINK_BLUE': b'\x98',
        'BLINK_YELLOW': b'\x99',
        'BLINK_CYAN': b'\x9A',
        'BLINK_MAGENTA': b'\x9B',
        'BLINK_WHITE': b'\x9C',
        'BLINK_RED_GREEN_BLUE_YELLOW_CYAN_MAGENTA_WHITE': b'\x95'
    }

    @staticmethod
    def get_code(name):
        return Effect.EFFECT_LIST.get(name)

    @staticmethod
    def get_effect_list():
        return list(Effect.EFFECT_LIST.keys())
