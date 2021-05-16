import logging
from config import Config
from bridge import Bridge
from device.led_rgb import LedRgb

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
_LOGGER = logging.getLogger('ha-bt')

_CONFIG = Config()


def run():
    bridge = Bridge(_CONFIG.MQTT)
    device = LedRgb(_CONFIG)
    device.connect(bridge)
    bridge.start()


if __name__ == '__main__':
    _LOGGER.info('HA-BT start')
    run()
