from threading import RLock
from typing import Callable, List

from .event import JagerEvent


EventHandler = Callable[
    [JagerEvent],
    None,
]


class EventBus:

    def __init__(self):

        self._handlers: List[
            EventHandler
        ] = []

        self._history: List[
            JagerEvent
        ] = []

        self._lock = RLock()

    def subscribe(
        self,
        handler: EventHandler,
    ):

        if not callable(handler):

            raise TypeError(
                "handler must be callable"
            )

        with self._lock:

            if handler not in self._handlers:

                self._handlers.append(
                    handler
                )

    def unsubscribe(
        self,
        handler: EventHandler,
    ):

        with self._lock:

            if handler in self._handlers:

                self._handlers.remove(
                    handler
                )

    def publish(
        self,
        event: JagerEvent,
    ):

        with self._lock:

            self._history.append(
                event
            )

            handlers = list(
                self._handlers
            )

        for handler in handlers:

            handler(event)

    def history(self):

        with self._lock:

            return list(
                self._history
            )

    def clear(self):

        with self._lock:

            self._history.clear()
