from collections import defaultdict
from threading import RLock
from typing import Dict


class RuntimeMetrics:

    def __init__(self):

        self._counters = defaultdict(
            int
        )

        self._values = {}

        self._lock = RLock()

    def increment(
        self,
        name: str,
        amount: int = 1,
    ):

        with self._lock:

            self._counters[
                name
            ] += amount

    def set(
        self,
        name: str,
        value,
    ):

        with self._lock:

            self._values[name] = value

    def get(
        self,
        name: str,
        default=0,
    ):

        with self._lock:

            if name in self._values:

                return self._values[name]

            return self._counters.get(
                name,
                default,
            )

    def snapshot(self) -> Dict:

        with self._lock:

            return {
                "counters":
                    dict(self._counters),
                "values":
                    dict(self._values),
            }

    def reset(self):

        with self._lock:

            self._counters.clear()
            self._values.clear()
