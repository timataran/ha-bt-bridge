import logging
from device.mitemp.connection import Connection
from device.error import BTConnectError

_LOGGER = logging.getLogger(__name__)


class Thermometer:
    def __init__(self, mac):
        self.connection = Connection(mac)

    def read(self):
        try:
            data = self.connection.read()

            return self._decode_data(data)

        except BTConnectError as err:
            _LOGGER.error(f'BT connection error: {err}')

    @staticmethod
    def _decode_data(data):
        temperature = round(int.from_bytes(data[0:2], byteorder='little', signed=True) / 100, 1)
        humidity = int.from_bytes(data[2:3], byteorder='little', signed=True)
        voltage = int.from_bytes(data[3:5], byteorder='little') / 1000
        battery_level = min(int(round((voltage - 2.1), 2) * 100), 100)

        return {
            "temperature": temperature,
            "humidity": humidity,
            "voltage": voltage,
            "battery": battery_level
        }
