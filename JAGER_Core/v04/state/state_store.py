from copy import deepcopy
from threading import RLock
from typing import Optional

from .runtime_state import RuntimeState


class StateStore:

    def __init__(
        self,
        state: Optional[
            RuntimeState
        ] = None,
    ):

        self._state = (
            state or RuntimeState()
        )

        self._lock = RLock()

    def get(self):

        with self._lock:

            return deepcopy(
                self._state
            )

    def update(
        self,
        state: RuntimeState,
    ):

        with self._lock:

            self._state = deepcopy(
                state
            )

    def mutate(
        self,
        callback,
    ):

        with self._lock:

            callback(self._state)

            return deepcopy(
                self._state
            )

    def snapshot(self):

        with self._lock:

            return self._state.to_dict()

    def reset(self):

        with self._lock:

            self._state = RuntimeState()
