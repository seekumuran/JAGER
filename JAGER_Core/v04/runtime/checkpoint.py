from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional


@dataclass
class RuntimeCheckpoint:

    checkpoint_id: str

    iteration: int

    status: str

    experiment_id: Optional[str] = None

    created_at: str = field(
        default_factory=lambda:
            datetime.now(
                timezone.utc
            ).isoformat()
    )

    state: Dict[str, Any] = field(
        default_factory=dict
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self):

        return {
            "checkpoint_id":
                self.checkpoint_id,
            "iteration":
                self.iteration,
            "status":
                self.status,
            "experiment_id":
                self.experiment_id,
            "created_at":
                self.created_at,
            "state":
                dict(self.state),
            "metadata":
                dict(self.metadata),
        }

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
    ):

        return cls(
            checkpoint_id=data[
                "checkpoint_id"
            ],
            iteration=data[
                "iteration"
            ],
            status=data[
                "status"
            ],
            experiment_id=data.get(
                "experiment_id"
            ),
            created_at=data.get(
                "created_at",
                datetime.now(
                    timezone.utc
                ).isoformat(),
            ),
            state=dict(
                data.get(
                    "state",
                    {},
                )
            ),
            metadata=dict(
                data.get(
                    "metadata",
                    {},
                )
            ),
        )
