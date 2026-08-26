from typing import Any, Dict

from .action import Action
from .target_controller import (
    TargetController,
)


class ActionAuthorizer:

    def __init__(
        self,
        targets: TargetController,
    ):

        self.targets = targets

    def authorize(
        self,
        action: Action,
    ) -> Dict[str, Any]:

        if not isinstance(
            action,
            Action,
        ):

            raise TypeError(
                "action must be Action"
            )

        if not action.target_id:

            return {
                "allowed": False,
                "reason":
                    "action has no target",
                "action_id":
                    action.action_id,
            }

        result = self.targets.authorize(
            target_id=action.target_id,
            action={
                "type":
                    action.action_type,
                "parameters":
                    action.parameters,
            },
            risk=action.risk,
        )

        result["action_id"] = (
            action.action_id
        )

        return result
