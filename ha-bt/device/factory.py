import logging
from device.led_rgb import LedRgb
from device.mitemp2 import MiTemp2

_LOGGER = logging.getLogger(__name__)


def build_device(device_config):
    device_type = device_config.type
    constructor = globals().get(device_type)
    if constructor is not None:
        return constructor(device_config)
    else:
        _LOGGER.error(f"Failed to build device by type '{device_type}'")
