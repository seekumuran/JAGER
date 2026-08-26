from typing import Any, Dict

from .event_manager import EventManager
from .telemetry_manager import (
    TelemetryManager,
)


class Observability:

    def __init__(
        self,
        events: EventManager,
    ):

        self.events = events

        self.telemetry = (
            TelemetryManager(
                events.bus
            )
        )

    def event(
        self,
        event_type: str,
        payload: Any = None,
        source: str = "runtime",
        metadata: Dict[str, Any] = None,
    ):

        return self.events.emit(
            event_type=event_type,
            payload=payload,
            source=source,
            metadata=metadata,
        )

    def metric(
        self,
        name: str,
        value: float,
        iteration: int = None,
    ):

        return self.telemetry.record(
            name=name,
            value=value,
            iteration=iteration,
        )

    def snapshot(self):

        return {
            "events":
                self.events.snapshot(),
            "telemetry":
                self.telemetry.snapshot(),
        }

    def persist(self):

        return self.telemetry.persist()
