import json
from pathlib import Path
from typing import Dict, List, Optional


class ExperimentMemory:

    def __init__(self, path="memory.json"):
        self.path = Path(path)
        self.records: List[Dict] = []

        self.load()

    def add(self, result):

        record = dict(result)

        record["memory_id"] = (
            len(self.records) + 1
        )

        self.records.append(record)

    def get(self, memory_id: int):

        for record in self.records:

            if record["memory_id"] == memory_id:
                return record

        return None

    def all(self):

        return list(self.records)

    def recent(self, limit=10):

        if limit <= 0:
            return []

        return self.records[-limit:]

    def search(
        self,
        target_name: Optional[str] = None,
        status: Optional[str] = None,
    ):

        results = []

        for record in self.records:

            if (
                target_name is not None
                and record.get(
                    "target_name"
                ) != target_name
            ):
                continue

            observation = record.get(
                "observation",
                {},
            )

            if (
                status is not None
                and observation.get(
                    "status"
                ) != status
            ):
                continue

            results.append(record)

        return results

    def save(self):

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self.path.open(
            "w",
            encoding="utf-8",
        ) as handle:

            json.dump(
                self.records,
                handle,
                indent=2,
                sort_keys=True,
            )

    def load(self):

        if not self.path.exists():
            return

        with self.path.open(
            "r",
            encoding="utf-8",
        ) as handle:

            data = json.load(handle)

        if not isinstance(data, list):
            raise ValueError(
                "Memory file must contain "
                "a JSON list."
            )

        self.records = data

    def clear(self):

        self.records.clear()

        if self.path.exists():
            self.path.unlink()
