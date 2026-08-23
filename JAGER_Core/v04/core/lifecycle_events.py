from typing import Any, Dict, Optional

from .event_bus import EventBus
from .event_types import (
    EXPERIMENT_COMPLETED,
    EXPERIMENT_CREATED,
    EXPERIMENT_FAILED,
    EXPERIMENT_STARTED,
    EXECUTION_COMPLETED,
    EXECUTION_FAILED,
    EXECUTION_STARTED,
    ITERATION_STARTED,
    RUNTIME_STARTED,
    RUNTIME_STOPPED,
)


class LifecycleEventEmitter:

    def __init__(
        self,
        event_bus: Optional[
            EventBus
        ] = None,
    ):

        self.events = (
            event_bus
            or EventBus()
        )

    def runtime_started(
        self,
        metadata: Optional[Dict] = None,
    ):

        return self.events.emit(
            RUNTIME_STARTED,
            source="runtime",
            metadata=metadata,
        )

    def runtime_stopped(
        self,
        metadata: Optional[Dict] = None,
    ):

        return self.events.emit(
            RUNTIME_STOPPED,
            source="runtime",
            metadata=metadata,
        )

    def experiment_created(
        self,
        experiment: Any,
    ):

        return self.events.emit(
            EXPERIMENT_CREATED,
            payload=self._serialize(
                experiment
            ),
            source="experiment",
        )

    def experiment_started(
        self,
        experiment: Any,
    ):

        return self.events.emit(
            EXPERIMENT_STARTED,
            payload=self._serialize(
                experiment
            ),
            source="experiment",
        )

    def experiment_completed(
        self,
        experiment: Any,
    ):

        return self.events.emit(
            EXPERIMENT_COMPLETED,
            payload=self._serialize(
                experiment
            ),
            source="experiment",
        )

    def experiment_failed(
        self,
        experiment: Any,
    ):

        return self.events.emit(
            EXPERIMENT_FAILED,
            payload=self._serialize(
                experiment
            ),
            source="experiment",
        )

    def iteration_started(
        self,
        context: Any,
    ):

        return self.events.emit(
            ITERATION_STARTED,
            payload=self._serialize(
                context
            ),
            source="iteration",
        )

    def execution_started(
        self,
        record: Any,
    ):

        return self.events.emit(
            EXECUTION_STARTED,
            payload=self._serialize(
                record
            ),
            source="execution",
        )

    def execution_completed(
        self,
        record: Any,
    ):

        return self.events.emit(
            EXECUTION_COMPLETED,
            payload=self._serialize(
                record
            ),
            source="execution",
        )

    def execution_failed(
        self,
        record: Any,
    ):

        return self.events.emit(
            EXECUTION_FAILED,
            payload=self._serialize(
                record
            ),
            source="execution",
        )

    @staticmethod
    def _serialize(
        value: Any,
    ):

        if value is None:

            return None

        if hasattr(
            value,
            "to_dict",
        ):

            return value.to_dict()

        if hasattr(
            value,
            "snapshot",
        ):

            return value.snapshot()

        if isinstance(
            value,
            dict,
        ):

            return dict(value)

        return value
