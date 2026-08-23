from typing import Dict, Optional

from .resource_budget import (
    ResourceBudget,
)

from .risk_budget import (
    RiskBudget,
)


class BudgetManager:

    def __init__(
        self,
        resources: Optional[
            ResourceBudget
        ] = None,
        risk: Optional[
            RiskBudget
        ] = None,
    ):

        self.resources = (
            resources
            or ResourceBudget()
        )

        self.risk = (
            risk
            or RiskBudget()
        )

    def begin_iteration(self):

        self.resources.consume_iteration()

    def record_failure(self):

        self.resources.consume_failure()

    def record_actions(
        self,
        count: int = 1,
    ):

        self.resources.consume_actions(
            count
        )

    def record_risk(
        self,
        amount: float,
    ):

        self.risk.consume(
            amount
        )

    def can_continue(self):

        return (
            self.resources.can_iterate()
            and self.resources.can_fail()
            and self.risk.available() > 0.0
        )

    def snapshot(self) -> Dict:

        return {
            "resources":
                self.resources.snapshot(),
            "risk":
                self.risk.snapshot(),
            "can_continue":
                self.can_continue(),
        }
