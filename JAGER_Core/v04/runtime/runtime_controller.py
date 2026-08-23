from typing import Any, Dict, Optional

from .budget_manager import (
    BudgetManager,
)

from .lifecycle import (
    RuntimeLifecycle,
)

from .termination import (
    TerminationController,
)


class RuntimeController:

    def __init__(
        self,
        budget: Optional[
            BudgetManager
        ] = None,
        termination: Optional[
            TerminationController
        ] = None,
    ):

        self.budget = (
            budget
            or BudgetManager()
        )

        self.termination = (
            termination
            or TerminationController()
        )

        self.lifecycle = (
            RuntimeLifecycle()
        )

    def start(self):

        self.lifecycle.start()

    def begin_iteration(self):

        if self.lifecycle.status != "running":

            raise RuntimeError(
                "runtime is not running"
            )

        self.budget.begin_iteration()

    def record_action(
        self,
        count: int = 1,
    ):

        self.budget.record_actions(
            count
        )

    def record_risk(
        self,
        amount: float,
    ):

        self.budget.record_risk(
            amount
        )

    def record_failure(self):

        self.budget.record_failure()

    def evaluate(
        self,
        iteration: int,
        score: Optional[float] = None,
        error: Optional[str] = None,
    ):

        decision = self.termination.evaluate(
            iteration=iteration,
            status=self.lifecycle.status,
            score=score,
            error=error,
        )

        if decision.should_stop:

            if decision.status == "failed":

                self.lifecycle.fail(
                    decision.reason
                )

            else:

                self.lifecycle.complete(
                    decision.reason
                )

        return decision

    def fail(
        self,
        reason: str,
    ):

        self.lifecycle.fail(reason)

    def cancel(
        self,
        reason: str = "cancelled",
    ):

        self.lifecycle.cancel(reason)

    def snapshot(self) -> Dict[str, Any]:

        return {
            "lifecycle":
                self.lifecycle.snapshot(),
            "budget":
                self.budget.snapshot(),
        }
