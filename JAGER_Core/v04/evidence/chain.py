from typing import Dict, List

from .event import EvidenceEvent


class EvidenceChain:

    REQUIRED_SEQUENCE = [
        "policy_evaluation",
        "decision",
        "action",
        "target_response",
    ]

    def __init__(
        self,
        events: List[
            EvidenceEvent
        ],
    ):

        self.events = list(events)

    def ordered(self):

        return sorted(
            self.events,
            key=lambda event:
                event.timestamp,
        )

    def event_types(self):

        return [
            event.event_type
            for event in self.ordered()
        ]

    def backbone_complete(self):

        types = self.event_types()

        position = 0

        for event_type in types:

            if (
                event_type
                == self.REQUIRED_SEQUENCE[
                    position
                ]
            ):

                position += 1

                if position == len(
                    self.REQUIRED_SEQUENCE
                ):
                    return True

        return False

    def missing(self):

        present = set(
            self.event_types()
        )

        return [
            event_type
            for event_type
            in self.REQUIRED_SEQUENCE
            if event_type not in present
        ]

    def to_dict(self):

        return {
            "event_count":
                len(self.events),
            "event_types":
                self.event_types(),
            "backbone_complete":
                self.backbone_complete(),
            "missing":
                self.missing(),
            "events": [
                event.to_dict()
                for event in self.ordered()
            ],
        }
