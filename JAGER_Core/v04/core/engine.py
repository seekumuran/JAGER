from typing import Any, Dict, Optional

from ..runtime.budget_manager import (
    BudgetManager,
)

from ..runtime.experiment_runtime import (
    ExperimentRuntime,
)

from ..runtime.termination import (
    TerminationController,
)

from .config import JagerConfig


class JagerEngine:

    def __init__(
        self,
        config: Optional[
            JagerConfig
        ] = None,
    ):

        self.config = (
            config
            or JagerConfig()
        )

        self.config.validate()

        self.budget = BudgetManager()

        self.runtime = ExperimentRuntime()

        self.termination = (
            TerminationController(
                target_score=
                    self.config.target_score,
                maximum_iterations=
                    self.config.max_iterations,
            )
        )

        self.started = False

    def start(self):

        if self.started:

            raise RuntimeError(
                "JAGER is already started"
            )

        self.started = True

        return self

    def stop(self):

        self.started = False

    def create_experiment(
        self,
        name: str,
        objective: str,
        target: str,
        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ):

        return self.runtime.create(
            name=name,
            objective=objective,
            target=target,
            metadata=metadata,
        )

    def run_iteration(
        self,
        experiment_id: str,
        iteration: int,
        action: Any,
        score: Optional[float] = None,
    ):

        if not self.started:

            raise RuntimeError(
                "JAGER is not started"
            )

        context = (
            self.runtime.begin_iteration(
                experiment_id,
                iteration,
            )
        )

        record = (
            self.runtime.begin_execution(
                action=action,
                iteration=iteration,
                experiment_id=experiment_id,
            )
        )

        return context, record, score

    def complete_execution(
        self,
        record,
        output: Any = None,
        duration_ms: Optional[
            float
        ] = None,
    ):

        return self.runtime.complete_execution(
            record,
            output=output,
            duration_ms=duration_ms,
        )

    def evaluate(
        self,
        experiment_id: str,
        iteration: int,
        score: Optional[float] = None,
        error: Optional[str] = None,
    ):

        return self.runtime.evaluate(
            experiment_id=experiment_id,
            iteration=iteration,
            score=score,
            error=error,
        )

    def snapshot(self):

        return {
            "config":
                self.config.to_dict(),
            "started":
                self.started,
            "runtime":
                self.runtime.snapshot(),
        }
