import time
from dataclasses import asdict, dataclass
from typing import Any, Dict, List


@dataclass
class ExperimentEvent:
    event_id: int
    timestamp: float
    event_type: str
    experiment_id: str
    trace_id: str
    payload: Dict[str, Any]


class ExperimentLogger:
    def __init__(self):
        self.events: List[ExperimentEvent] = []
        self._counter = 0

    def record(
        self,
        event_type,
        experiment_id,
        trace_id,
        payload=None,
    ):
        self._counter += 1

        event = ExperimentEvent(
            event_id=self._counter,
            timestamp=time.time(),
            event_type=event_type,
            experiment_id=experiment_id,
            trace_id=trace_id,
            payload=payload or {},
        )

        self.events.append(event)

        return event

    def action(
        self,
        experiment_id,
        trace_id,
        action,
    ):
        return self.record(
            "ACTION",
            experiment_id,
            trace_id,
            {
                "action_id": action.action_id,
                "operation": action.operation,
                "parameters": action.parameters,
            },
        )

    def observation(
        self,
        experiment_id,
        trace_id,
        observation,
    ):
        return self.record(
            "OBSERVATION",
            experiment_id,
            trace_id,
            {
                "observation_id": observation.observation_id,
                "status": observation.status,
                "telemetry": observation.telemetry,
            },
        )

    def decision(
        self,
        experiment_id,
        trace_id,
        decision,
    ):
        return self.record(
            "DECISION",
            experiment_id,
            trace_id,
            {
                "allowed": decision.allowed,
                "reason": decision.reason,
                "risk": decision.risk,
                "confidence": decision.confidence,
            },
        )

    def export(self):
        return [
            asdict(event)
            for event in self.events
        ]
