from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class ExecutionResult:

    success: bool

    status: str

    output: Any = None

    error: Optional[str] = None

    duration_ms: Optional[float] = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    def is_successful(self):
        return self.success

    def is_failed(self):
        return not self.success

    def to_dict(self):

        return {
            "success": self.success,
            "status": self.status,
            "output": self.output,
            "error": self.error,
            "duration_ms": self.duration_ms,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def success_result(
        cls,
        output=None,
        duration_ms=None,
        metadata=None,
    ):

        return cls(
            success=True,
            status="completed",
            output=output,
            duration_ms=duration_ms,
            metadata=dict(
                metadata or {}
            ),
        )

    @classmethod
    def failure_result(
        cls,
        error,
        duration_ms=None,
        metadata=None,
    ):

        return cls(
            success=False,
            status="failed",
            error=str(error),
            duration_ms=duration_ms,
            metadata=dict(
                metadata or {}
            ),
        )
