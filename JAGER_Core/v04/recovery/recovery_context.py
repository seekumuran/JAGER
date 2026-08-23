from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class RecoveryContext:

    experiment_id: str

    attempt: int = 0

    recovered: bool = False

    failure_count: int = 0

    metadata: Dict[
        str,
        Any,
    ] = field(
        default_factory=dict
    )

    def record_failure(
        self,
        error: str,
    ):

        self.failure_count += 1

        self.metadata[
            "last_error"
        ] = error

    def record_recovery(
        self,
    ):

        self.recovered = True

        self.attempt += 1

    def to_dict(self):

        return {
            "experiment_id":
                self.experiment_id,
            "attempt":
                self.attempt,
            "recovered":
                self.recovered,
            "failure_count":
                self.failure_count,
            "metadata":
                dict(self.metadata),
        }
