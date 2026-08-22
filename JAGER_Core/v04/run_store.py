import json
from pathlib import Path


class RunStore:

    def __init__(self, directory="runs"):
        self.directory = Path(directory)
        self.directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def save(self, run_id, data):
        path = self.directory / (
            f"{run_id}.json"
        )

        with path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                data,
                file,
                indent=2,
                sort_keys=True,
                default=str,
            )

        return path

    def load(self, run_id):
        path = self.directory / (
            f"{run_id}.json"
        )

        if not path.exists():
            raise FileNotFoundError(
                f"Run not found: {run_id}"
            )

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    def exists(self, run_id):
        return (
            self.directory
            / f"{run_id}.json"
        ).exists()

    def list_runs(self):
        return sorted(
            path.stem
            for path in self.directory.glob(
                "*.json"
            )
        )
