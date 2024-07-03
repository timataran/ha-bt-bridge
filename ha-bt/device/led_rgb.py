from device.base import DeviceBase
from device.led.driver import Led, Effect
from device.led.state import State


class LedRgb(DeviceBase):
    def __init__(self, config):
        super().__init__(config)
        self.driver = Led(config.MAC)
        self.state = State(config.MAC)
        self.config_topic = self._build_topic('config')
        self.state_topic = self._build_topic('state')
        self.command_topic = self._build_topic('set')

    def _connect_to_bridge(self):
        self.bridge.add_listener(self.command_topic, self.on_state_update_received)
        self._send_discovery_configs()
        self._send_state_to_driver()

    def on_state_update_received(self, state_update):
        self.state.update(state_update)
        self._send_state_to_driver()
        self._send_state_to_bridge()

    def _send_discovery_configs(self):
        self._send_discovery_to_bridge()
        self._send_state_to_bridge()

    def _send_discovery_to_bridge(self):
        config = {
            "schema": "json",
            "name": self.config.name,
            "command_topic": self.command_topic,
            "state_topic": self.state_topic,
            "unique_id": self.config.unique_id,
            "brightness": True,
            "brightness_scale": 100,
            "rgb": True,
            "effect": True,
            "effect_list": Effect.get_effect_list()
        }
        self.bridge.send(self.config_topic, config)

    def _send_state_to_bridge(self):
        last_state = self.state.read()
        if last_state is not None:
            self.bridge.send(self.state_topic, last_state)

    def _send_state_to_driver(self):
        state_update = self.state.get_update()
        if state_update is not None:
            self.driver.set_state(state_update)

    def _build_topic(self, name):
        return f'{self.config.discovery_prefix}/light/{self.config.unique_id}/{name}'
