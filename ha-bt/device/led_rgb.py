from device.led.driver import Led, Effect


class LedRgb:
    def __init__(self, config):
        self.config = config
        self.driver = Led(config.MAC)
        self.config_topic = self._build_topic('config')
        self.state_topic = self._build_topic('state')
        self.command_topic = self._build_topic('set')
        self.bridge = None

    def connect(self, bridge):
        self.bridge = bridge
        self.bridge.add_listener(self.command_topic, self.on_state_update_received)

        self._send_discovery_config()

    def on_state_update_received(self, state):
        self.driver.set_state(state)
        if state.get('color') is not None:
            state['effect'] = None
        self._send_new_state(state)

    def _send_discovery_config(self):
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

    def _send_new_state(self, state):
        self.bridge.send(self.state_topic, state)

    def _build_topic(self, name):
        return f'{self.config.discovery_prefix}/light/{self.config.unique_id}/{name}'
