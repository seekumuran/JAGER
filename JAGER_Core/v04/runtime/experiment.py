from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import time
import uuid


@dataclass
class Experiment:

    experiment_id: str
    target: str
    hypothesis: str

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    created_at: float = field(
        default_factory=time.time
    )

    status: str = "created"

    @classmethod
    def create(
        cls,
        target: str,
        hypothesis: str,
        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ):

        return cls(
            experiment_id=str(
                uuid.uuid4()
            ),
            target=target,
            hypothesis=hypothesis,
            metadata=dict(
                metadata or {}
            ),
        )

    def start(self):

        if self.status != "created":
            raise RuntimeError(
                "Experiment cannot be started "
                f"from state '{self.status}'"
            )

        self.status = "running"

    def complete(self):

        if self.status != "running":
            raise RuntimeError(
                "Experiment cannot be completed "
                f"from state '{self.status}'"
            )

        self.status = "completed"

    def fail(self):

        if self.status not in {
            "running",
            "created",
        }:
            raise RuntimeError(
                "Experiment cannot fail "
                f"from state '{self.status}'"
            )

        self.status = "failed"

    def to_dict(self):

        return {
            "experiment_id":
                self.experiment_id,
            "target":
                self.target,
            "hypothesis":
                self.hypothesis,
            "metadata":
                dict(self.metadata),
            "created_at":
                self.created_at,
            "status":
                self.status,
        }
