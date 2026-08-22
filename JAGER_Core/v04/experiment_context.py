from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class ExperimentContext:

    experiment_id: str
    target_name: str
    action: Dict[str, Any]
    observation: Dict[str, Any] = field(
        default_factory=dict
    )

    reward: float = 0.0
    novelty: float = 0.0

    success: bool = False

    def record_observation(
        self,
        observation,
    ):
        self.observation = observation

        self.success = (
            observation.get("status")
            != "FAILED"
        )

    def to_dict(self):

        return {
            "experiment_id":
                self.experiment_id,

            "target_name":
                self.target_name,

            "action":
                self.action,

            "observation":
                self.observation,

            "reward":
                self.reward,

            "novelty":
                self.novelty,

            "success":
                self.success,
        }
