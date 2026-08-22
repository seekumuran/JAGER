import json
from pathlib import Path
from typing import List

from .event import SecurityEvent


class EventLogger:

    def __init__(
        self,
        path="runs/events.jsonl",
    ):

        self.path = Path(path)

    def write(
        self,
        event: SecurityEvent,
    ):

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self.path.open(
            "a",
            encoding="utf-8",
        ) as handle:

            handle.write(
                json.dumps(
                    event.to_dict(),
                    sort_keys=True,
                )
            )

            handle.write("\n")

    def read(self) -> List[dict]:

        if not self.path.exists():
            return []

        events = []

        with self.path.open(
            "r",
            encoding="utf-8",
        ) as handle:

            for line in handle:

                line = line.strip()

                if not line:
                    continue

                events.append(
                    json.loads(line)
                )

        return events
