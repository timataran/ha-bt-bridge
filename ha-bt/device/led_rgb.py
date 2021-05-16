from device.led.driver import Led, Effect


class LedRgb:
    def __init__(self, config):
        self.config = config
        self.driver = Led(config.MAC)
        self.config_topic = 'homeassistant/light/rgb_stripe_one/config'
        self.state_topic = 'homeassistant/light/rgb_stripe_one/state'
        self.command_topic = 'homeassistant/light/rgb_stripe_one/set'
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
            "name": "RGB stripe test",
            "command_topic": self.command_topic,
            "state_topic": self.state_topic,
            "unique_id": "rgb_stripe_one",
            "brightness": True,
            "brightness_scale": 100,
            "rgb": True,
            "effect": True,
            "effect_list": Effect.get_effect_list()
        }
        self.bridge.send(self.config_topic, config)

    def _send_new_state(self, state):
        self.bridge.send(self.state_topic, state)
