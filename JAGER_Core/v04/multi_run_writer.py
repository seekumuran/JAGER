import json
from pathlib import Path


class MultiRunWriter:

    def __init__(
        self,
        directory="runs",
    ):
        self.directory = Path(
            directory
        )

        self.directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def write(
        self,
        experiment,
        filename="multi_run.json",
    ):

        path = (
            self.directory
            / filename
        )

        with path.open(
            "w",
            encoding="utf-8",
        ) as handle:

            json.dump(
                experiment.to_dict(),
                handle,
                indent=2,
                sort_keys=True,
            )

        return path
