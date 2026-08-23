from typing import Any, Dict, Optional

from .event_bus import EventBus
from .event_logger import EventLogger
from .event_store import EventStore
from .lifecycle_events import (
    LifecycleEventEmitter,
)


class EventManager:

    def __init__(
        self,
        store: Optional[
            EventStore
        ] = None,
    ):

        self.bus = EventBus()

        self.logger = EventLogger(
            self.bus
        )

        self.store = (
            store
            or EventStore()
        )

        self.lifecycle = (
            LifecycleEventEmitter(
                self.bus
            )
        )

    def emit(
        self,
        event_type: str,
        payload: Any = None,
        source: str = "runtime",
        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ):

        results = self.bus.emit(
            event_type=event_type,
            payload=payload,
            source=source,
            metadata=metadata,
        )

        latest = self.logger.latest()

        if latest is not None:

            self.store.append(
                latest
            )

        return results

    def subscribe(
        self,
        event_type: str,
        handler,
    ):

        return self.bus.subscribe(
            event_type,
            handler,
        )

    def unsubscribe(
        self,
        event_type: str,
        handler,
    ):

        self.bus.unsubscribe(
            event_type,
            handler,
        )

    def history(self):

        return self.logger.all()

    def snapshot(self):

        return self.logger.snapshot()
