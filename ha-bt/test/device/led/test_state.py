from unittest import TestCase
from device.led.state import State, DB_FILE
from pathlib import Path


class TestState(TestCase):
    def setUp(self) -> None:
        self._del_db_file()
        State("default-mac")

    def test_restore_saved_state(self):
        state = State("mac-value")
        initial_state = {"key1": "value1", "key2": "value2"}
        state.update(initial_state)

        state = State("mac-value")
        restored_state = state.read()

        self.assertDictEqual(initial_state, restored_state)

    def test_override_state(self):
        state = State("mac-value")
        state.update({"key1": "value1"})
        state.update({"key1": "value2"})

        restored_state = state.read()

        self.assertDictEqual({"key1": "value2"}, restored_state)

    def test_merge_state_on_update(self):
        state = State("mac-value")
        state.update({'state': 'ON', 'brightness': 52})
        state.update({"state": "ON", "color": {"r": 0, "g": 63, "b": 255}})

        self.assertDictEqual(
            {
                'state': 'ON',
                'brightness': 52,
                'color': {"r": 0, "g": 63, "b": 255}
            },
            state.read())

    def test_apply_off_filter_on_read(self):
        state = State("mac-value")
        state.update({'state': 'ON', "color": {"r": 3, "g": 3, "b": 3}})
        state.update({"state": "OFF", 'effect': 'MAGENTA'})

        self.assertDictEqual(
            {'state': 'OFF'},
            state.read()
        )

    def test_suppress_effect_in_value_ws_color(self):
        state = State("mac-value")
        state.update({'state': 'ON', "color": {"r": 3, "g": 3, "b": 3}})
        state.update({"state": "ON", 'effect': 'MAGENTA', "color": {"r": 0, "g": 63, "b": 255}})

        self.assertDictEqual(
            {
                'state': 'ON',
                'color': {"r": 0, "g": 63, "b": 255}
            },
            state.read())

    def test_suppress_effect_on_update_ws_color(self):
        state = State("mac-value")
        state.update({'state': 'ON', 'effect': 'MAGENTA'})
        state.update({"state": "ON", "color": {"r": 0, "g": 63, "b": 255}})

        self.assertDictEqual(
            {
                'state': 'ON',
                'color': {"r": 0, "g": 63, "b": 255}
            },
            state.read())

    def test_suppress_color_on_update_ws_effect(self):
        state = State("mac-value")
        state.update({"state": "ON", 'brightness': 52, "color": {"r": 0, "g": 63, "b": 255}})
        state.update({'state': 'ON', 'effect': 'MAGENTA'})

        self.assertDictEqual(
            {
                'state': 'ON',
                'brightness': 52,
                'effect': 'MAGENTA'
            },
            state.read())

    def test_store_states_by_mac(self):
        State("mac1").update({"name": "Alice"})
        State("mac2").update({"name": "Bob"})

        self.assertDictEqual({"name": "Alice"}, State("mac1").read())
        self.assertDictEqual({"name": "Bob"}, State("mac2").read())

    def test_return_none_on_no_saved_value(self):
        state = State("non-existent-mac")

        self.assertIsNone(state.read())

    def test_not_raise_on_db_error(self):
        self._set_db_read_only()
        with self.assertLogs('device.led.state', level='ERROR'):
            State("mac1")

    def test_write_log_on_db_error(self):
        self._set_db_read_only()
        with self.assertLogs('device.led.state', level='ERROR') as log_context:
            State("mac1")

        self.assertEqual(
            ['ERROR:device.led.state:Led-rgb state persistence failure: unable to open database file'],
            log_context.output
        )

    def tearDown(self) -> None:
        self._del_db_file()

    @classmethod
    def _set_db_read_only(cls):
        path = Path(DB_FILE)
        path.chmod(0o000)

    @classmethod
    def _del_db_file(cls):
        path = Path(DB_FILE)
        path.unlink(True)
