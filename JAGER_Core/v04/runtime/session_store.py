import json
from pathlib import Path
from typing import List

from .session import RuntimeSession


class SessionStore:

    def __init__(
        self,
        path: str = "data/sessions.json",
    ):

        self.path = Path(path)

    def save(
        self,
        sessions: List[
            RuntimeSession
        ],
    ):

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        payload = [
            session.snapshot()
            for session
            in sessions
        ]

        temporary = self.path.with_suffix(
            ".tmp"
        )

        with temporary.open(
            "w",
            encoding="utf-8",
        ) as handle:

            json.dump(
                payload,
                handle,
                indent=2,
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
