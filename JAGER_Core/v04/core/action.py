from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import uuid


@dataclass
class Action:

    action_type: str

    target_id: Optional[str] = None

    parameters: Dict[
        str,
        Any
    ] = field(
        default_factory=dict
    )

    risk: float = 0.0

    action_id: str = field(
        default_factory=lambda:
            str(uuid.uuid4())
    )

    metadata: Dict[
        str,
        Any
    ] = field(
        default_factory=dict
    )

    def to_dict(self):

        return {
            "action_id":
                self.action_id,
            "action_type":
                self.action_type,
            "target_id":
                self.target_id,
            "parameters":
                dict(self.parameters),
            "risk":
                self.risk,
            "metadata":
                dict(self.metadata),
        }
