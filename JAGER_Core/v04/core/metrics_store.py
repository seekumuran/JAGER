import json
from pathlib import Path
from typing import Dict, Any


class MetricsStore:

    def __init__(
        self,
        path: str = "data/metrics.json",
    ):

        self.path = Path(path)

    def save(
        self,
        metrics: Dict[str, Any],
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
                metrics,
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
