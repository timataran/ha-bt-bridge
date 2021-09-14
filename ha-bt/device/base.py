import logging
import schedule

_LOGGER = logging.getLogger(__name__)


class DeviceBase:
    def __init__(self, config):
        self.config = config
        self.bridge = None

    def connect(self, bridge):
        self.bridge = bridge
        self._connect_to_bridge()
        _LOGGER.info(f"{self.config.type} device with MAC {self.config.MAC} connected to bridge")
        self._schedule_discovery_send()

    def _schedule_discovery_send(self):
        schedule.every(self.config.discovery_period).seconds.do(self._send_discovery_configs)

    def _connect_to_bridge(self):
        pass

    def _send_discovery_configs(self):
        pass
