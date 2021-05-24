import bluepy.btle
from bluepy.btle import BTLEDisconnectError
from device.error import BTConnectError


class Connection:
    def __init__(self, mac):
        self.mac = mac
        self.device = None
        self.handle = None

    def get_handle(self):
        try:
            if self.handle is not None:
                return self.handle
            else:
                return self._fetch_handle_from_device()
        except BTLEDisconnectError as error:
            raise BTConnectError(f"{error}")

    def disconnect(self):
        if self.device is not None:
            self.device.disconnect()
            self.device = None
            self.handle = None

    def _fetch_handle_from_device(self):
        self.device = bluepy.btle.Peripheral(self.mac)
        characteristics = self.device.getCharacteristics()

        for handle in characteristics:
            if handle.propertiesToString().find('WRITE') >= 0:
                self.handle = handle
                return handle

        raise BTConnectError('failed to retrieve writable attribute')
