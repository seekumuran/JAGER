from typing import Any, Dict, Iterable, List, Optional

from .policy import (
    PolicyDecision,
    PolicyRule,
)


class PolicyEngine:

    def __init__(
        self,
        rules: Optional[
            Iterable[PolicyRule]
        ] = None,
    ):

        self.rules: List[
            PolicyRule
        ] = list(
            rules or []
        )

    def add_rule(
        self,
        rule: PolicyRule,
    ):

        if not isinstance(
            rule,
            PolicyRule,
        ):

            raise TypeError(
                "rule must be PolicyRule"
            )

        self.rules.append(
            rule
        )

        return rule

    def remove_rule(
        self,
        name: str,
    ):

        self.rules = [
            rule
            for rule in self.rules
            if rule.name != name
        ]

    def evaluate(
        self,
        action: Any,
        risk: float = 0.0,
    ) -> PolicyDecision:

        try:

            risk = float(risk)

        except (
            TypeError,
            ValueError,
        ):

            return PolicyDecision(
                allowed=False,
                reason="invalid risk value",
                action=action,
                risk=0.0,
            )

        if risk < 0.0:

            return PolicyDecision(
                allowed=False,
                reason="risk cannot be negative",
                action=action,
                risk=risk,
            )

        for rule in self.rules:

            decision = rule.evaluate(
                action,
                risk,
            )

            if decision is not None:

                return decision

        return PolicyDecision(
            allowed=True,
            reason="allowed by policy",
            action=action,
            risk=risk,
        )

    def check(
        self,
        action: Any,
        risk: float = 0.0,
    ) -> bool:

        return self.evaluate(
            action,
            risk,
        ).allowed

    def snapshot(self) -> Dict[str, Any]:

        return {
            "rules": [
                {
                    "name": rule.name,
                    "enabled":
                        rule.enabled,
                    "maximum_risk":
                        rule.maximum_risk,
                    "blocked_actions":
                        list(
                            rule.blocked_actions
                        ),
                    "required_fields":
                        list(
                            rule.required_fields
                        ),
                }
                for rule in self.rules
            ]
        }
