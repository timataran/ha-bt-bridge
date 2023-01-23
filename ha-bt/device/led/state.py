import sqlite3
import json
import logging

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
    @with_connection
    def __init__(self, mac: str, connection=None):
        self.mac = mac
        cur = connection.cursor()
        cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='last_known_state'")
        if cur.fetchone()[0] != 1:
            cur.execute("CREATE TABLE last_known_state (mac TEXT PRIMARY KEY, state TEXT)")

    @with_connection
    def write(self, state: dict, connection=None) -> None:
        state_json = json.dumps(state)
        cur = connection.cursor()
        cur.execute('''
        INSERT INTO last_known_state (mac,state) VALUES (?,?)
            ON CONFLICT DO UPDATE SET state=?
        ''', (self.mac, state_json, state_json))

    @with_connection
    def read(self, connection=None) -> dict:
        cur = connection.cursor()
        cur.execute("SELECT state FROM last_known_state WHERE mac=?", (self.mac,))
        data = cur.fetchone()
        if data is not None:
            return json.loads(data[0])
        else:
            return
