import json
from pathlib import Path


class ExperimentReplay:
    def __init__(self, result_file):
        self.result_file = Path(result_file)

    def load(self):
        with self.result_file.open(
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    def experiments(self):
        data = self.load()
        return data.get("experiments", [])

    def events(self):
        data = self.load()
        return data.get("events", [])

    def discoveries(self):
        data = self.load()
        return data.get("discoveries", [])

    def summary(self):
        data = self.load()

        return {
            "run_id": data.get("run_id"),
            "seed": data.get("seed"),
            "budget": data.get("budget"),
            "experiments": len(
                data.get("experiments", [])
            ),
            "events": len(
                data.get("events", [])
            ),
            "discoveries": len(
                data.get("discoveries", [])
            ),
            "memory_size": data.get(
                "memory_size",
                0,
            ),
        }
