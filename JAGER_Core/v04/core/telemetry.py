from typing import Any, Dict, Optional

from .event_bus import EventBus
from .event import JagerEvent
from .metrics import MetricsRegistry


class Telemetry:

    def __init__(
        self,
        event_bus: EventBus,
        metrics: Optional[
            MetricsRegistry
        ] = None,
    ):

        self.events = event_bus

        self.metrics = (
            metrics
            or MetricsRegistry()
        )

        self.events.subscribe(
            "*",
            self._consume,
        )

    def _consume(
        self,
        event: JagerEvent,
    ):

        payload = event.payload

        if not isinstance(
            payload,
            dict,
        ):

            return

        metrics = payload.get(
            "metrics"
        )

        if not isinstance(
            metrics,
            dict,
        ):

            return

        iteration = payload.get(
            "iteration"
        )

        for name, value in metrics.items():

            if isinstance(
                value,
                (int, float),
            ):

                self.metrics.record(
                    name,
                    value,
                    iteration=iteration,
                )

    def record(
        self,
        name: str,
        value: float,
        iteration: Optional[int] = None,
    ):

        return self.metrics.record(
            name,
            value,
            iteration,
        )

    def snapshot(self):

        return self.metrics.snapshot()
