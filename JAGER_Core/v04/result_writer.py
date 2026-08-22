import json
from pathlib import Path


class ResultWriter:

    def __init__(self, directory="runs"):
        self.directory = Path(directory)
        self.directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def write(
        self,
        run,
        filename=None,
    ):
        if filename is None:
            filename = (
                f"{run.summary.run_id}.json"
            )

        path = self.directory / filename

        with path.open(
            "w",
            encoding="utf-8",
        ) as handle:
            json.dump(
                run.to_dict(),
                handle,
                indent=2,
                sort_keys=True,
            )

        return path

    def read(self, filename):
        path = self.directory / filename

        with path.open(
            "r",
            encoding="utf-8",
        ) as handle:
            return json.load(handle)
