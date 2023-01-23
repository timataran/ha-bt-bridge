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
        state.write(initial_state)

        state = State("mac-value")
        restored_state = state.read()

        self.assertDictEqual(initial_state, restored_state)

    def test_override_state(self):
        state = State("mac-value")
        state.write({"key1": "value1"})
        state.write({"key1": "value2"})

        restored_state = state.read()

        self.assertDictEqual({"key1": "value2"}, restored_state)

    def test_store_states_by_mac(self):
        State("mac1").write({"name": "Alice"})
        State("mac2").write({"name": "Bob"})

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
