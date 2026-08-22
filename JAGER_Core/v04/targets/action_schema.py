from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class TargetAction:

    type: str
    parameters: Dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self):
        return {
            "type": self.type,
            "parameters": self.parameters,
        }


@dataclass
class ActionValidation:

    valid: bool
    reason: str
    normalized: Dict[str, Any] | None = None

    def to_dict(self):
        return {
            "valid": self.valid,
            "reason": self.reason,
            "normalized": self.normalized,
        }


class ActionSchema:

    COMMON_FIELDS = {
        "operation",
    }

    TARGET_OPERATIONS = {
        "blackbox": {
            "observe",
            "probe",
            "system_observation",
        },
        "linux": {
            "observe",
            "system_observation",
            "process_count",
        },
        "ai_sandbox": {
            "observe",
            "prompt_observation",
        },
    }

    def validate(
        self,
        target: str,
        action: Dict[str, Any],
    ) -> ActionValidation:

        if not isinstance(action, dict):

            return ActionValidation(
                False,
                "Action must be a dictionary.",
            )

        action_type = action.get("type")

        if not isinstance(
            action_type,
            str,
        ) or not action_type.strip():

            return ActionValidation(
                False,
                "Action type is required.",
            )

        parameters = action.get(
            "parameters",
            {},
        )

        if not isinstance(
            parameters,
            dict,
        ):

            return ActionValidation(
                False,
                "Action parameters must "
                "be a dictionary.",
            )

        operation = parameters.get(
            "operation",
            "observe",
        )

        allowed = self.TARGET_OPERATIONS.get(
            target
        )

        if allowed is None:

            return ActionValidation(
                False,
                f"Unknown target: {target}",
            )

        if operation not in allowed:

            return ActionValidation(
                False,
                (
                    f"Operation '{operation}' "
                    f"is not supported by "
                    f"target '{target}'."
                ),
            )

        normalized = {
            "type": action_type,
            "parameters": dict(parameters),
        }

        normalized[
            "parameters"
        ].setdefault(
            "operation",
            operation,
        )

        return ActionValidation(
            True,
            "Action is valid.",
            normalized,
        )

    def operations_for(
        self,
        target: str,
    ) -> List[str]:

        return sorted(
            self.TARGET_OPERATIONS.get(
                target,
                set(),
            )
        )
