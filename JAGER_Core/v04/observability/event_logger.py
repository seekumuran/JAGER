import json
from pathlib import Path

from .event import JagerEvent


class EventLogger:

    def __init__(
        self,
        path: str,
    ):

        self.path = Path(path)

    def handle(
        self,
        event: JagerEvent,
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
                    default=str,
                )
            )

            handle.write("\n")
