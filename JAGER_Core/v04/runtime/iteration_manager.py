from typing import Any, Dict, Optional

from .iteration_context import (
    IterationContext,
)

from .iteration_history import (
    IterationHistory,
)


class IterationManager:

    def __init__(
        self,
        history: Optional[
            IterationHistory
        ] = None,
    ):

        self.history = (
            history
            or IterationHistory()
        )

    def start(
        self,
        experiment_id: str,
        iteration: int,
        target: str,
        objective: str,
        state: Optional[
            Dict[str, Any]
        ] = None,
    ) -> IterationContext:

        context = IterationContext(
            experiment_id=experiment_id,
            iteration=iteration,
            target=target,
            objective=objective,
            state=dict(
                state or {}
            ),
        )

        self.history.add(
            context
        )

        return context

    def current(self):

        return self.history.latest()

    def complete(
        self,
        context: IterationContext,
        state: Optional[
            Dict[str, Any]
        ] = None,
    ):

        if state:

            context.update_state(
                state
            )

        context.set_metadata(
            "status",
            "completed",
        )

        return context

    def fail(
        self,
        context: IterationContext,
        error: Exception | str,
    ):

        context.record_error(
            error
        )

        context.set_metadata(
            "status",
            "failed",
        )

        return context

    def snapshot(self):

        return self.history.to_dict()
