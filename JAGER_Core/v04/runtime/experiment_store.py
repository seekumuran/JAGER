import json
from pathlib import Path
from typing import List

from .experiment import Experiment


class ExperimentStore:

    def __init__(
        self,
        path: str = "data/experiments.json",
    ):

        self.path = Path(path)

    def save(
        self,
        experiments: List[Experiment],
    ):

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        payload = [
            experiment.to_dict()
            for experiment
            in experiments
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
