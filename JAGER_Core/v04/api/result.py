from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class JagerResult:

    raw: Dict[str, Any]

    @property
    def iterations(self):

        return self.raw.get(
            "iterations",
            0,
        )

    @property
    def history(self):

        return self.raw.get(
            "history",
            [],
        )

    @property
    def final_plan(self):

        return self.raw.get(
            "final_plan"
        )

    def succeeded(self):

        if not self.history:
            return False

        return any(
            item["result"].succeeded()
            for item in self.history
        )

    def discoveries(self):

        return [
            item["result"].discovery
            for item in self.history
            if item["result"].discovery
            is not None
        ]

    def experiences(self):

        return [
            item["result"].experience
            for item in self.history
            if item["result"].experience
            is not None
        ]

    def to_dict(self):

        return self.raw
