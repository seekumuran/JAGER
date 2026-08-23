from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class PolicyContext:

    experiment_id: str
    target: str
    action_type: str

    parameters: Dict[str, Any] = field(
        default_factory=dict
    )

    actor: str = "jager"
    environment: Dict[str, Any] = field(
        default_factory=dict
    )

    risk_level: str = "unknown"

    def to_dict(self):

        return {
            "experiment_id":
                self.experiment_id,
            "target":
                self.target,
            "action_type":
                self.action_type,
            "parameters":
                dict(self.parameters),
            "actor":
                self.actor,
            "environment":
                dict(self.environment),
            "risk_level":
                self.risk_level,
        }
