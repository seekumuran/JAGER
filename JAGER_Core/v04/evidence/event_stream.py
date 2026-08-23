from typing import Callable, List, Optional

from .event import EvidenceEvent


class EvidenceEventStream:

    def __init__(self):

        self.events: List[
            EvidenceEvent
        ] = []

        self.subscribers: List[
            Callable[[EvidenceEvent], None]
        ] = []

    def publish(
        self,
        event: EvidenceEvent,
    ):

        self.events.append(event)

        for subscriber in list(
            self.subscribers
        ):

            subscriber(event)

        return event

    def subscribe(
        self,
        callback: Callable[
            [EvidenceEvent], None
        ],
    ):

        if callback not in self.subscribers:
            self.subscribers.append(
                callback
            )

    def unsubscribe(
        self,
        callback: Callable[
            [EvidenceEvent], None
        ],
    ):

        if callback in self.subscribers:
            self.subscribers.remove(
                callback
            )

    def by_type(
        self,
        event_type: str,
    ):

        return [
            event
            for event in self.events
            if event.event_type
            == event_type
        ]

    def by_experiment(
        self,
        experiment_id: str,
    ):

        return [
            event
            for event in self.events
            if event.experiment_id
            == experiment_id
        ]

    def latest(
        self,
    ) -> Optional[EvidenceEvent]:

        if not self.events:
            return None

        return self.events[-1]

    def size(self):

        return len(self.events)

    def clear(self):

        self.events.clear()
