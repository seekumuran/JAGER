from typing import Any

from .policy_engine import PolicyEngine
from .target import TargetRegistry


class PolicyTargetController:

    def __init__(
        self,
        policies: PolicyEngine,
        targets: TargetRegistry,
    ):

        self.policies = policies
        self.targets = targets

    def authorize(
        self,
        target_id: str,
        action: Any,
        risk: float = 0.0,
    ):

        target = self.targets.get(
            target_id
        )

        if target is None:

            return {
                "allowed": False,
                "reason":
                    "target not found",
                "target_id":
                    target_id,
            }

        if not target.active:

            return {
                "allowed": False,
                "reason":
                    "target inactive",
                "target_id":
                    target_id,
            }

        decision = (
            self.policies.evaluate(
                action,
                risk,
            )
        )

        result = decision.to_dict()

        result["target_id"] = (
            target_id
        )

        return result
