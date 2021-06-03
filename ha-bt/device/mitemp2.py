import logging
from timeout_decorator import timeout, TimeoutError
import schedule
from device.base import DeviceBase
from device.mitemp.driver import Thermometer

_LOGGER = logging.getLogger(__name__)


class MiTemp2(DeviceBase):
    def __init__(self, config):
        super().__init__(config)
        self.state_topic = self._build_topic(self.config.unique_id, 'state')

    def _connect_to_bridge(self):
        self._send_discovery_configs()
        self._send_status()
        self._schedule_status_send()

    def _send_status(self):
        try:
            data = self._read_status()
            if data is not None:
                _LOGGER.debug(f'Send {self.config.unique_id} data: {data}')
                self.bridge.send(self.state_topic, data)
        except TimeoutError as err:
            _LOGGER.error(err)

    def _read_status(self):
        timeout_value = hasattr(self.config, 'read_timeout') if self.config.read_timeout is not None else 10
        by_signals = hasattr(self.config, 'timeout_by_signals') if self.config.timeout_by_signals is not None else False

        @timeout(timeout_value, use_signals=by_signals)
        def read_with_timeout():
            device = Thermometer(self.config.MAC)
            return device.read()

        return read_with_timeout()

    def _send_discovery_configs(self):
        for topic, config in self._get_config_topics():
            self.bridge.send(topic, config)

    def _get_config_topics(self):
        measurement_map = {
            "temperature": "°C",
            "humidity": "%",
            "voltage": "V",
            "battery": "%"
        }
        for parameter, measurement in measurement_map.items():
            yield (
                self._build_topic(f'{self.config.unique_id}_{parameter}', 'config'),
                {
                    "state_topic": self.state_topic,
                    "name": f'{self.config.name} {parameter}',
                    "device_class": parameter,
                    "unit_of_measurement": measurement,
                    "value_template": f"{{{{value_json.{parameter}}}}}"
                }
            )

    def _build_topic(self, unique_id, name):
        return f'{self.config.discovery_prefix}/sensor/{unique_id}/{name}'

    def _schedule_status_send(self):
        schedule.every(self.config.poll_period).seconds.do(self._send_status)
