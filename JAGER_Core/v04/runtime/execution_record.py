from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional


@dataclass
class ExecutionRecord:

    execution_id: str

    experiment_id: Optional[str]

    iteration: int

    action: Any

    result: Any = None

    status: str = "created"

    created_at: str = field(
        default_factory=lambda:
            datetime.now(
                timezone.utc
            ).isoformat()
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    def complete(
        self,
        result=None,
    ):

        self.result = result
        self.status = "completed"

    def fail(
        self,
        result=None,
    ):

        self.result = result
        self.status = "failed"

    def to_dict(self):

        return {
            "execution_id":
                self.execution_id,
            "experiment_id":
                self.experiment_id,
            "iteration":
                self.iteration,
            "action":
                self.action,
            "result":
                self.result,
            "status":
                self.status,
            "created_at":
                self.created_at,
            "metadata":
                dict(self.metadata),
        }
