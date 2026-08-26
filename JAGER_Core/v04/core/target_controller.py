from typing import Any, Dict, Optional

from .policy_engine import PolicyEngine
from .policy_target import (
    PolicyTargetController,
)
from .target import (
    Target,
    TargetRegistry,
)


class TargetController:

    def __init__(
        self,
        policies: Optional[
            PolicyEngine
        ] = None,
        targets: Optional[
            TargetRegistry
        ] = None,
    ):

        self.policies = (
            policies
            or PolicyEngine()
        )

        self.targets = (
            targets
            or TargetRegistry()
        )

        self.authorization = (
            PolicyTargetController(
                self.policies,
                self.targets,
            )
        )

    def register(
        self,
        target: Target,
    ):

        return self.targets.register(
            target
        )

    def get(
        self,
        target_id: str,
    ):

        return self.targets.get(
            target_id
        )

    def remove(
        self,
        target_id: str,
    ):

        return self.targets.remove(
            target_id
        )

    def activate(
        self,
        target_id: str,
    ):

        target = self.get(
            target_id
        )

        if target is None:

            raise KeyError(
                target_id
            )

        target.activate()

        return target

    def deactivate(
        self,
        target_id: str,
    ):

        target = self.get(
            target_id
        )

        if target is None:

            raise KeyError(
                target_id
            )

        target.deactivate()

        return target

    def authorize(
        self,
        target_id: str,
        action: Any,
        risk: float = 0.0,
    ):

        return self.authorization.authorize(
            target_id=target_id,
            action=action,
            risk=risk,
        )

    def list_targets(self):

        return self.targets.all()

    def active_targets(self):

        return self.targets.active()

    def snapshot(
        self,
    ) -> Dict[str, Any]:

        return {
            "targets":
                self.targets.snapshot(),
            "policies":
                self.policies.snapshot(),
        }
