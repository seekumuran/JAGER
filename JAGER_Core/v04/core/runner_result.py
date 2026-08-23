from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class RunnerResult:

    experiment_id: str

    iterations: int

    completed: int = 0

    stopped: bool = False

    results: List[Any] = field(
        default_factory=list
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    @property
    def successful(self):

        return [
            item
            for item in self.results
            if "error" not in item
        ]

    @property
    def failed(self):

        return [
            item
            for item in self.results
            if "error" in item
        ]

    def add(
        self,
        result: Any,
    ):

        self.results.append(
            result
        )

        self.completed = len(
            self.results
        )

    def to_dict(self):

        return {
            "experiment_id":
                self.experiment_id,
            "iterations":
                self.iterations,
            "completed":
                self.completed,
            "stopped":
                self.stopped,
            "results":
                list(self.results),
            "metadata":
                dict(self.metadata),
        }
