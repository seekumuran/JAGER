from collections import defaultdict
from typing import Any, Callable, Dict, List

from .event import JagerEvent


class EventBus:

    def __init__(self):

        self._handlers: Dict[
            str,
            List[Callable]
        ] = defaultdict(list)

        self._history: List[
            JagerEvent
        ] = []

    def subscribe(
        self,
        event_type: str,
        handler: Callable,
    ):

        if not callable(handler):

            raise TypeError(
                "handler must be callable"
            )

        if handler not in self._handlers[
            event_type
        ]:

            self._handlers[
                event_type
            ].append(handler)

        return handler

    def unsubscribe(
        self,
        event_type: str,
        handler: Callable,
    ):

        handlers = self._handlers.get(
            event_type,
            [],
        )

        if handler in handlers:

            handlers.remove(handler)

        if not handlers:

            self._handlers.pop(
                event_type,
                None,
            )

    def publish(
        self,
        event: JagerEvent,
    ):

        self._history.append(
            event
        )

        handlers = list(
            self._handlers.get(
                event.event_type,
                [],
            )
        )

        handlers += list(
            self._handlers.get(
                "*",
                [],
            )
        )

        results = []

        for handler in handlers:

            results.append(
                handler(event)
            )

        return results

    def emit(
        self,
        event_type: str,
        payload: Any = None,
        source: str = "runtime",
        metadata: Dict[str, Any] = None,
    ):

        event = JagerEvent(
            event_type=event_type,
            source=source,
            payload=payload,
            metadata=dict(
                metadata or {}
            ),
        )

        return self.publish(
            event
        )

    def history(self):

        return list(
            self._history
        )

    def clear_history(self):

        self._history.clear()

    def handlers(self):

        return {
            event_type: list(
                handlers
            )
            for event_type, handlers
            in self._handlers.items()
        }
