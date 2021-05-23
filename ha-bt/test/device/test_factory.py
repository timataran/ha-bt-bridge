from unittest import TestCase
import device.factory as factory


class TestDeviceFactory(TestCase):

    def test_build_led_rgb(self):
        config = LedRgbConfig()
        device = factory.build_device(config)
        self.assertEqual("<class 'device.led_rgb.LedRgb'>", str(type(device)))

    def test_build_mitemp(self):
        config = MiTemp2Config()
        device = factory.build_device(config)
        self.assertEqual("<class 'device.mitemp2.MiTemp2'>", str(type(device)))

    def test_return_none_on_type_unknown(self):
        config = UnknownTypeConfig()

        with self.assertLogs('device.factory', level='DEBUG'):
            device = factory.build_device(config)

        self.assertIsNone(device)

    def test_log_error_on_device_build_failure(self):
        config = UnknownTypeConfig()

        with self.assertLogs('device.factory', level='DEBUG') as log_context:
            factory.build_device(config)

        self.assertEqual(
            ["ERROR:device.factory:Failed to build device by type 'Unknown'"],
            log_context.output
        )


class LedRgbConfig:
    type = 'LedRgb'
    MAC = 'a4:c1:38:15:91:10'
    discovery_prefix = 'homeassistant'
    unique_id = 'led_device'
    name = 'Friendly led name'


class MiTemp2Config:
    type = 'MiTemp2'
    MAC = 'a4:c1:38:15:91:10'
    discovery_prefix = 'homeassistant'
    unique_id = 'temp_sensor_device'
    name = 'Friendly sensor name'
    poll_period = 180


class UnknownTypeConfig:
    type = 'Unknown'
