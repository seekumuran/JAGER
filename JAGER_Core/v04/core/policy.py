from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PolicyDecision:

    allowed: bool

    reason: str

    action: Any = None

    risk: float = 0.0

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self):

        return {
            "allowed": self.allowed,
            "reason": self.reason,
            "action": self.action,
            "risk": self.risk,
            "metadata": dict(self.metadata),
        }


@dataclass
class PolicyRule:

    name: str

    enabled: bool = True

    maximum_risk: Optional[
        float
    ] = None

    blocked_actions: List[
        str
    ] = field(
        default_factory=list
    )

    required_fields: List[
        str
    ] = field(
        default_factory=list
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    def evaluate(
        self,
        action: Any,
        risk: float = 0.0,
    ) -> Optional[
        PolicyDecision
    ]:

        if not self.enabled:

            return None

        if (
            self.maximum_risk
            is not None
            and risk > self.maximum_risk
        ):

            return PolicyDecision(
                allowed=False,
                reason=(
                    f"risk exceeds rule "
                    f"'{self.name}'"
                ),
                action=action,
                risk=risk,
            )

        action_type = None

        if isinstance(
            action,
            dict,
        ):

            action_type = action.get(
                "type"
            )

        if (
            action_type
            and action_type
            in self.blocked_actions
        ):

            return PolicyDecision(
                allowed=False,
                reason=(
                    f"action '{action_type}' "
                    f"is blocked"
                ),
                action=action,
                risk=risk,
            )

        if isinstance(
            action,
            dict,
        ):

            missing = [
                field
                for field
                in self.required_fields
                if field not in action
            ]

            if missing:

                return PolicyDecision(
                    allowed=False,
                    reason=(
                        "required fields "
                        f"missing: {missing}"
                    ),
                    action=action,
                    risk=risk,
                )

        return None
