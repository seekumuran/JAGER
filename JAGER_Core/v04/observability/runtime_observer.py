from typing import Any, Dict, Optional

from .event import JagerEvent
from .event_bus import EventBus
from .metrics import RuntimeMetrics
from .tracer import RuntimeTracer


class RuntimeObserver:

    def __init__(
        self,
        event_bus: Optional[
            EventBus
        ] = None,
        metrics: Optional[
            RuntimeMetrics
        ] = None,
        tracer: Optional[
            RuntimeTracer
        ] = None,
    ):

        self.events = (
            event_bus
            or EventBus()
        )

        self.metrics = (
            metrics
            or RuntimeMetrics()
        )

        self.tracer = (
            tracer
            or RuntimeTracer()
        )

    def emit(
        self,
        event_type: str,
        payload: Optional[
            Dict[str, Any]
        ] = None,
        experiment_id: Optional[
            str
        ] = None,
    ):

        event = JagerEvent(
            event_type=event_type,
            experiment_id=experiment_id,
            payload=dict(
                payload or {}
            ),
        )

        self.events.publish(event)

        self.metrics.increment(
            f"events.{event_type}"
        )

        return event

    def experiment_started(
        self,
        experiment_id: str,
    ):

        self.metrics.increment(
            "experiments.started"
        )

        return self.emit(
            event_type="experiment_started",
            experiment_id=experiment_id,
        )

    def experiment_completed(
        self,
        experiment_id: str,
    ):

        self.metrics.increment(
            "experiments.completed"
        )

        return self.emit(
            event_type="experiment_completed",
            experiment_id=experiment_id,
        )

    def experiment_failed(
        self,
        experiment_id: str,
        error: str,
    ):

        self.metrics.increment(
            "experiments.failed"
        )

        return self.emit(
            event_type="experiment_failed",
            experiment_id=experiment_id,
            payload={
                "error": error,
            },
        )

    def discovery(
        self,
        experiment_id: str,
        discovery: Any,
    ):

        self.metrics.increment(
            "discoveries.found"
        )

        return self.emit(
            event_type="discovery_found",
            experiment_id=experiment_id,
            payload={
                "discovery": discovery,
            },
        )

    def experience(
        self,
        experiment_id: str,
        experience: Any,
    ):

        self.metrics.increment(
            "experiences.created"
        )

        return self.emit(
            event_type="experience_created",
            experiment_id=experiment_id,
            payload={
                "experience": experience,
            },
        )

    def snapshot(self):

        return {
            "metrics":
                self.metrics.snapshot(),
            "events": [
                event.to_dict()
                for event
                in self.events.history()
            ],
            "traces":
                self.tracer.snapshot(),
        }
