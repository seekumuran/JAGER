from datetime import datetime, timezone
from typing import Any, Dict, List

from .event import JagerEvent
from .event_bus import EventBus


class EventLogger:

    def __init__(
        self,
        event_bus: EventBus,
    ):

        self.events = event_bus

        self.records: List[
            Dict[str, Any]
        ] = []

        self.events.subscribe(
            "*",
            self._receive,
        )

    def _receive(
        self,
        event: JagerEvent,
    ):

        record = {
            "event_id":
                event.event_id,
            "event_type":
                event.event_type,
            "source":
                event.source,
            "timestamp":
                event.timestamp,
            "payload":
                event.payload,
            "metadata":
                dict(event.metadata),
            "recorded_at":
                datetime.now(
                    timezone.utc
                ).isoformat(),
        }

        self.records.append(
            record
        )

        return record

    def all(self):

        return list(
            self.records
        )

    def latest(self):

        if not self.records:

            return None

        return self.records[-1]

    def count(self):

        return len(
            self.records
        )

    def clear(self):

        self.records.clear()

    def snapshot(self):

        return {
            "count": self.count(),
            "events": self.all(),
        }
