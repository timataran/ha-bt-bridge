import logging

_LOGGER = logging.getLogger(__name__)


class MiTemp2:
    def __init__(self, config):
        self.config = config
        self.bridge = None

    def connect(self, bridge):
        self.bridge = bridge
