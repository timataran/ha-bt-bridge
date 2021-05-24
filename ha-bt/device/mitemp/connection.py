from bluepy.btle import Peripheral, DefaultDelegate, BTLEDisconnectError
from device.error import BTConnectError


class Connection:
    def __init__(self, mac):
        self.mac = mac

    def read(self):
        received_data = []

        class NotificationHandler(DefaultDelegate):
            def __init__(self):
                DefaultDelegate.__init__(self)

            def handleNotification(self, _, data):
                received_data.append(data)

        device = None

        try:
            device = Peripheral(self.mac)
            device.writeCharacteristic(0x0038, b'\x01\x00', True)
            device.writeCharacteristic(0x0046, b'\xf4\x01\x00', True)
            device.withDelegate(NotificationHandler())
            device.waitForNotifications(10)

            if len(received_data) > 0:
                return received_data.pop()
            else:
                raise BTConnectError('Failed to retrieve sensor data')

        except BTLEDisconnectError as error:
            raise BTConnectError(f"{error}")

        finally:
            if device is not None:
                device.disconnect()
