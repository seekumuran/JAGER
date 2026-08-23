from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass(frozen=True)
class Action:

    action_id: str
    action_type: str
    target: str

    parameters: Dict[str, Any] = field(
        default_factory=dict
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self):

        return {
            "action_id": self.action_id,
            "action_type": self.action_type,
            "target": self.target,
            "parameters": dict(
                self.parameters
            ),
            "metadata": dict(
                self.metadata
            ),
        }
