import schedule
import time
from threading import Thread


class JobRunner:
    def __init__(self, config):
        self.config = config

    def start(self):
        thread = Thread(target=self._loop)
        thread.daemon = True
        thread.start()

    def _loop(self):
        while True:
            schedule.run_pending()
            time.sleep(self.config.sleep_seconds)
