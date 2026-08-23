import json
from pathlib import Path
from typing import Any, Dict, List


class EventStore:

    def __init__(
        self,
        path: str = "data/events.json",
    ):

        self.path = Path(path)

    def save(
        self,
        events: List[
            Dict[str, Any]
        ],
    ):

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        temporary = self.path.with_suffix(
            ".tmp"
        )

        with temporary.open(
            "w",
            encoding="utf-8",
        ) as handle:

            json.dump(
                events,
                handle,
                indent=2,
                default=str,
            )

        temporary.replace(
            self.path
        )

    def load(self):

        if not self.path.exists():

            return []

        with self.path.open(
            "r",
            encoding="utf-8",
        ) as handle:

            return json.load(handle)

    def append(
        self,
        event: Dict[str, Any],
    ):

        events = self.load()

        events.append(event)

        self.save(events)

        return event
