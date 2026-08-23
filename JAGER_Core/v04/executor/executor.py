import time
import uuid
from typing import Any, Dict, Optional

from .action import Action
from .result import ExecutionResult
from .registry import TargetRegistry


class ExperimentExecutor:

    def __init__(
        self,
        registry: TargetRegistry,
    ):

        self.registry = registry

    def create_action(
        self,
        target: str,
        action_type: str,
        parameters: Optional[
            Dict[str, Any]
        ] = None,
        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ):

        return Action(
            action_id=str(
                uuid.uuid4()
            ),
            action_type=action_type,
            target=target,
            parameters=dict(
                parameters or {}
            ),
            metadata=dict(
                metadata or {}
            ),
        )

    def execute(
        self,
        action: Action,
    ) -> ExecutionResult:

        target = self.registry.get(
            action.target
        )

        started = time.perf_counter()

        try:

            output = target.execute(
                action.action_type,
                dict(action.parameters),
            )

            status = "success"
            error = None

        except Exception as exc:

            output = None
            status = "error"
            error = (
                f"{type(exc).__name__}: "
                f"{exc}"
            )

        duration_ms = (
            time.perf_counter()
            - started
        ) * 1000.0

        return ExecutionResult(
            action_id=action.action_id,
            target=action.target,
            status=status,
            duration_ms=duration_ms,
            output=output,
            error=error,
        )

    def observe(
        self,
        target_name: str,
    ):

        target = self.registry.get(
            target_name
        )

        return target.observe()
