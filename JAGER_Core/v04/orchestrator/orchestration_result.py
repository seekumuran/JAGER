from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class OrchestrationResult:

    status: str

    experiment_id: str

    action: Optional[Any] = None
    execution: Optional[Any] = None
    discovery: Optional[Any] = None
    experience: Optional[Any] = None

    reason: str = ""

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    def succeeded(self):

        return self.status == "success"

    def to_dict(self):

        return {
            "status":
                self.status,
            "experiment_id":
                self.experiment_id,
            "action":
                (
                    self.action.to_dict()
                    if hasattr(
                        self.action,
                        "to_dict"
                    )
                    else self.action
                ),
            "execution":
                (
                    self.execution.to_dict()
                    if hasattr(
                        self.execution,
                        "to_dict"
                    )
                    else self.execution
                ),
            "discovery":
                (
                    self.discovery.to_dict()
                    if hasattr(
                        self.discovery,
                        "to_dict"
                    )
                    else self.discovery
                ),
            "experience":
                (
                    self.experience.to_dict()
                    if hasattr(
                        self.experience,
                        "to_dict"
                    )
                    else self.experience
                ),
            "reason":
                self.reason,
            "metadata":
                dict(self.metadata),
        }
