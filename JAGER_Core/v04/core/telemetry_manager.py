from typing import Any, Dict, Optional

from .event_bus import EventBus
from .metrics import MetricsRegistry
from .telemetry import Telemetry
from .telemetry_store import TelemetryStore


class TelemetryManager:

    def __init__(
        self,
        event_bus: EventBus,
        store: Optional[
            TelemetryStore
        ] = None,
    ):

        self.store = (
            store
            or TelemetryStore()
        )

        self.telemetry = Telemetry(
            event_bus
        )

        self._events_seen = 0

        event_bus.subscribe(
            "*",
            self._count_event,
        )

    def _count_event(
        self,
        event,
    ):

        self._events_seen += 1

    @property
    def metrics(self) -> MetricsRegistry:

        return self.telemetry.metrics

    def record(
        self,
        name: str,
        value: float,
        iteration: Optional[
            int
        ] = None,
    ):

        return self.telemetry.record(
            name=name,
            value=value,
            iteration=iteration,
        )

    def persist(self):

        snapshot = self.snapshot()

        self.store.save(
            snapshot
        )

        return snapshot

    def load(self):

        return self.store.load()

    def snapshot(self):

        return {
            "events_seen":
                self._events_seen,
            "metrics":
                self.telemetry.snapshot(),
        }

    def reset(self):

        self.metrics.clear()

        self._events_seen = 0
