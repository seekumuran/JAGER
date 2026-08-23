from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional


@dataclass
class PolicyRule:
    rule_id: str
    description: str
    effect: str
    priority: int = 0
    conditions: Dict[str, Any] = field(
        default_factory=dict
    )
    evaluator: Optional[
        Callable[[Dict[str, Any]], bool]
    ] = None

    def __post_init__(self):
        if self.effect not in {
            "ALLOW",
            "DENY",
        }:
            raise ValueError(
                "effect must be ALLOW or DENY"
            )

    def matches(
        self,
        context: Dict[str, Any],
    ) -> bool:

        if self.evaluator is not None:
            return bool(
                self.evaluator(context)
            )

        for key, expected in (
            self.conditions.items()
        ):

            if context.get(key) != expected:
                return False

        return True

    def to_dict(self):

        return {
            "rule_id": self.rule_id,
            "description":
                self.description,
            "effect": self.effect,
            "priority": self.priority,
            "conditions":
                dict(self.conditions),
        }
