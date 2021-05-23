import logging
from config_loader import ConfigLoader
from timer import JobRunner
from bridge import Bridge
from device.led_rgb import LedRgb

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
_LOGGER = logging.getLogger('ha-bt')


def run():
    config = ConfigLoader().load('./configuration.yaml')

    job_runner = JobRunner(config.timer)
    job_runner.start()

    bridge = Bridge(config.MQTT)
    for device_config in config.devices:
        device = LedRgb(device_config)
        device.connect(bridge)
    bridge.start()


if __name__ == '__main__':
    _LOGGER.info('HA-BT start')
    run()
