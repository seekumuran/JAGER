from typing import Any, Dict, Optional

from .experiment_manager import (
    ExperimentManager,
)

from .iteration_manager import (
    IterationManager,
)

from .execution_manager import (
    ExecutionManager,
)

from .runtime_controller import (
    RuntimeController,
)


class ExperimentRuntime:

    def __init__(
        self,
        experiments: Optional[
            ExperimentManager
        ] = None,
        iterations: Optional[
            IterationManager
        ] = None,
        executions: Optional[
            ExecutionManager
        ] = None,
        controller: Optional[
            RuntimeController
        ] = None,
    ):

        self.experiments = (
            experiments
            or ExperimentManager()
        )

        self.iterations = (
            iterations
            or IterationManager()
        )

        self.executions = (
            executions
            or ExecutionManager()
        )

        self.controller = (
            controller
            or RuntimeController()
        )

    def create(
        self,
        name: str,
        objective: str,
        target: str,
        metadata: Optional[Dict] = None,
    ):

        return self.experiments.create(
            name=name,
            objective=objective,
            target=target,
            metadata=metadata,
        )

    def start(
        self,
        experiment_id: str,
    ):

        experiment = (
            self.experiments.start(
                experiment_id
            )
        )

        self.controller.start()

        return experiment

    def begin_iteration(
        self,
        experiment_id: str,
        iteration: int,
    ):

        experiment = (
            self.experiments.get(
                experiment_id
            )
        )

        if experiment is None:

            raise KeyError(
                f"unknown experiment: "
                f"{experiment_id}"
            )

        self.controller.begin_iteration()

        return self.iterations.start(
            experiment_id=experiment_id,
            iteration=iteration,
            target=experiment.target,
            objective=experiment.objective,
        )

    def begin_execution(
        self,
        action: Any,
        iteration: int,
        experiment_id: Optional[str] = None,
    ):

        self.controller.record_action()

        return self.executions.begin(
            action=action,
            iteration=iteration,
            experiment_id=experiment_id,
        )

    def complete_execution(
        self,
        record,
        output=None,
        duration_ms=None,
    ):

        return self.executions.complete(
            record,
            output=output,
            duration_ms=duration_ms,
        )

    def fail_execution(
        self,
        record,
        error,
        duration_ms=None,
    ):

        self.controller.record_failure()

        return self.executions.fail(
            record,
            error=error,
            duration_ms=duration_ms,
        )

    def evaluate(
        self,
        experiment_id: str,
        iteration: int,
        score=None,
        error=None,
    ):

        decision = self.controller.evaluate(
            iteration=iteration,
            score=score,
            error=error,
        )

        if decision.should_stop:

            if decision.status == "completed":

                self.experiments.complete(
                    experiment_id,
                    result={
                        "score": score,
                        "reason":
                            decision.reason,
                    },
                )

            else:

                self.experiments.fail(
                    experiment_id,
                    decision.reason,
                )

        return decision

    def snapshot(self):

        return {
            "experiments":
                self.experiments.snapshot(),
            "iterations":
                self.iterations.snapshot(),
            "executions":
                self.executions.snapshot(),
            "runtime":
                self.controller.snapshot(),
        }
