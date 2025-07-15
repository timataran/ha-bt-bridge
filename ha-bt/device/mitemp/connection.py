from bluepy.btle import Peripheral, DefaultDelegate, BTLEDisconnectError
from device.error import BTConnectError

_FIRMWARE_VERSION_HANDLE = 0x12
_V2_DATA_HANDLE = 0x33


class Connection:
    def __init__(self, mac):
        self.mac = mac

    def read(self):
        device = None

        try:
            device = Peripheral(self.mac)
            version = self._get_device_version(device)

            return self.get_v1_data(device) if version == 1 else self.get_v2_data(device)

        except BTLEDisconnectError as error:
            raise BTConnectError(f"{error}")

        finally:
            if device is not None:
                device.disconnect()

    @staticmethod
    def _get_device_version(device):
        hex_value = device.readCharacteristic(_FIRMWARE_VERSION_HANDLE)
        version = str(hex_value, 'utf-8')

        if version.startswith('1.'):
            return 1
        elif version.startswith('2.'):
            return 2
        else:
            raise BTConnectError(f"Unknown device version: {version}")

    @staticmethod
    def get_v1_data(device):
        received_data = []

        class NotificationHandler(DefaultDelegate):
            def __init__(self):
                DefaultDelegate.__init__(self)

            def handleNotification(self, _, data):
                received_data.append(data)

        device.writeCharacteristic(0x0038, b'\x01\x00', True)
        device.writeCharacteristic(0x0046, b'\xf4\x01\x00', True)
        device.withDelegate(NotificationHandler())
        device.waitForNotifications(10)

        if len(received_data) > 0:
            return received_data.pop()
        else:
            raise BTConnectError('Failed to retrieve sensor data')

    @staticmethod
    def get_v2_data(device):
        return device.readCharacteristic(_V2_DATA_HANDLE)
