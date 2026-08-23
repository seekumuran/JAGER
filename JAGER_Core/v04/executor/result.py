from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class ExecutionResult:

    action_id: str
    target: str
    status: str
    duration_ms: float

    output: Any = None

    error: Optional[str] = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    def succeeded(self):

        return self.status == "success"

    def failed(self):

        return not self.succeeded()

    def to_dict(self):

        return {
            "action_id": self.action_id,
            "target": self.target,
            "status": self.status,
            "duration_ms":
                self.duration_ms,
            "output": self.output,
            "error": self.error,
            "metadata":
                dict(self.metadata),
        }
