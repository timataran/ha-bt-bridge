import sqlite3
import json
import logging
from typing import Optional

DB_FILE = 'data/led_rgb_state.db'
_LOGGER = logging.getLogger(__name__)


def with_connection(method):
    def wrapper(*args, **kwargs):
        try:
            with sqlite3.connect(DB_FILE) as con:
                return method(*args, connection=con, **kwargs)
        except sqlite3.Error as err:
            _LOGGER.error(f'Led-rgb state persistence failure: {err}')

    return wrapper


class State:
    def __init__(self, mac: str):
        self.mac: str = mac
        self.value: Optional[dict] = None
        self._init_db()

    def update(self, state_update: dict) -> None:
        self.read()
        self._merge_update(state_update)
        self._write_to_db()

    def read(self) -> Optional[dict]:
        if self.value is None:
            self.value = self._read_from_db()

        return self.value

    def _merge_update(self, state_update: dict) -> None:
        if self.value is None:
            self.value = {}

        if state_update.get('color') is not None:
            self.value.pop('effect', None)

        if state_update.get('effect') is not None:
            self.value.pop('color', None)

        self.value = self.value | state_update

    @with_connection
    def _init_db(self, connection=None) -> None:
        cur = connection.cursor()
        cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='last_known_state'")
        if cur.fetchone()[0] != 1:
            cur.execute("CREATE TABLE last_known_state (mac TEXT PRIMARY KEY, state TEXT)")

    @with_connection
    def _read_from_db(self, connection=None) -> Optional[dict]:
        cur = connection.cursor()
        cur.execute("SELECT state FROM last_known_state WHERE mac=?", (self.mac,))
        data = cur.fetchone()
        if data is not None:
            return json.loads(data[0])
        else:
            return

    @with_connection
    def _write_to_db(self, connection=None) -> None:
        state_json = json.dumps(self.value)
        cur = connection.cursor()
        cur.execute(
            '''INSERT INTO last_known_state (mac,state) VALUES (?,?)
                    ON CONFLICT(mac) DO UPDATE SET state=excluded.state''',
            (self.mac, state_json)
        )
