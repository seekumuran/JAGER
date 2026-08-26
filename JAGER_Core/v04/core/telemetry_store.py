import json
from pathlib import Path
from typing import Any, Dict, Optional


class TelemetryStore:

    def __init__(
        self,
        path: str = "data/telemetry.json",
    ):

        self.path = Path(path)

    def _ensure_parent(self):

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    def save(
        self,
        telemetry: Dict[str, Any],
    ):

        self._ensure_parent()

        temporary = self.path.with_suffix(
            ".tmp"
        )

        with temporary.open(
            "w",
            encoding="utf-8",
        ) as handle:

            json.dump(
                telemetry,
                handle,
                indent=2,
                default=str,
            )

        temporary.replace(
            self.path
        )

    def load(self):

        if not self.path.exists():

            return {}

        with self.path.open(
            "r",
            encoding="utf-8",
        ) as handle:

            return json.load(handle)

    def update(
        self,
        values: Dict[str, Any],
    ):

        current = self.load()

        current.update(values)

        self.save(current)

        return current

    def exists(self):

        return self.path.exists()

    def delete(self):

        if self.path.exists():

            self.path.unlink()
