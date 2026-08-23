from dataclasses import dataclass, field
from typing import Any, Dict, List
import uuid


@dataclass
class Goal:

    goal_id: str
    target: str
    objective: str

    constraints: Dict[str, Any] = field(
        default_factory=dict
    )

    success_criteria: List[str] = field(
        default_factory=list
    )

    priority: float = 0.5

    @classmethod
    def create(
        cls,
        target: str,
        objective: str,
        constraints=None,
        success_criteria=None,
        priority: float = 0.5,
    ):

        return cls(
            goal_id=str(uuid.uuid4()),
            target=target,
            objective=objective,
            constraints=dict(
                constraints or {}
            ),
            success_criteria=list(
                success_criteria or []
            ),
            priority=max(
                0.0,
                min(1.0, float(priority)),
            ),
        )

    def to_dict(self):

        return {
            "goal_id": self.goal_id,
            "target": self.target,
            "objective": self.objective,
            "constraints":
                dict(self.constraints),
            "success_criteria":
                list(self.success_criteria),
            "priority": self.priority,
        }
