from typing import Optional

from .policy_context import PolicyContext
from .policy_decision import PolicyDecision
from .policy_engine import PolicyEngine


class PolicyMediator:

    def __init__(
        self,
        engine: PolicyEngine,
    ):

        self.engine = engine

    def evaluate(
        self,
        context: PolicyContext,
    ) -> PolicyDecision:

        return self.engine.evaluate(
            context.to_dict()
        )

    def authorize(
        self,
        context: PolicyContext,
    ) -> bool:

        decision = self.evaluate(
            context
        )

        return decision.allowed

    def require_authorization(
        self,
        context: PolicyContext,
    ) -> PolicyDecision:

        decision = self.evaluate(
            context
        )

        if not decision.allowed:
            raise PermissionError(
                (
                    "JÄGER action denied: "
                    f"{decision.reason}"
                )
            )

        return decision
