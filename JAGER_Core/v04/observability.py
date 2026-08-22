import uuid
from typing import List

from .models import Event


class EventLogger:
    def __init__(self):
        self.events: List[Event] = []

    def emit(
        self,
        trace_id: str,
        event_type: str,
        operation: str,
        decision: str,
        reason: str,
        metadata=None,
    ):
        event = Event(
            event_id=f"evt-{uuid.uuid4().hex[:12]}",
            trace_id=trace_id,
            event_type=event_type,
            operation=operation,
            decision=decision,
            reason=reason,
            metadata=metadata or {},
        )

        self.events.append(event)

        return event

    def export(self):
        return [
            {
                "event_id": event.event_id,
                "trace_id": event.trace_id,
                "event_type": event.event_type,
                "operation": event.operation,
                "decision": event.decision,
                "reason": event.reason,
                "metadata": event.metadata,
            }
            for event in self.events
        ]
