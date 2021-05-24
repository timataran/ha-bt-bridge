import logging

_LOGGER = logging.getLogger(__name__)


class DeviceBase:
    def __init__(self, config):
        self.config = config
        self.bridge = None

    def connect(self, bridge):
        self.bridge = bridge
        self._connect_to_bridge()
        _LOGGER.info(f"{self.config.type} device with MAC {self.config.MAC} connected to bridge")

    def _connect_to_bridge(self):
        pass
