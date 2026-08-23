import uuid
from typing import Any, Dict, Optional

from .execution_history import (
    ExecutionHistory,
)

from .execution_record import (
    ExecutionRecord,
)

from .execution_result import (
    ExecutionResult,
)


class ExecutionManager:

    def __init__(
        self,
        history: Optional[
            ExecutionHistory
        ] = None,
    ):

        self.history = (
            history
            or ExecutionHistory()
        )

    def begin(
        self,
        action: Any,
        iteration: int,
        experiment_id: Optional[str] = None,
        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ):

        record = ExecutionRecord(
            execution_id=str(
                uuid.uuid4()
            ),
            experiment_id=experiment_id,
            iteration=iteration,
            action=action,
            metadata=dict(
                metadata or {}
            ),
        )

        self.history.add(
            record
        )

        return record

    def complete(
        self,
        record: ExecutionRecord,
        output: Any = None,
        duration_ms: Optional[
            float
        ] = None,
    ):

        result = (
            ExecutionResult.success_result(
                output=output,
                duration_ms=duration_ms,
            )
        )

        record.complete(
            result.to_dict()
        )

        return result

    def fail(
        self,
        record: ExecutionRecord,
        error: Any,
        duration_ms: Optional[
            float
        ] = None,
    ):

        result = (
            ExecutionResult.failure_result(
                error=error,
                duration_ms=duration_ms,
            )
        )

        record.fail(
            result.to_dict()
        )

        return result

    def latest(self):

        return self.history.latest()

    def snapshot(self):

        return self.history.snapshot()
