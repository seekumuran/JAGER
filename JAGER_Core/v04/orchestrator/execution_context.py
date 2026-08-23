from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class ExecutionContext:

    experiment_id: str
    target: str
    hypothesis: str

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    baseline: Optional[
        Dict[str, Any]
    ] = None

    previous_experiences: list = field(
        default_factory=list
    )

    observations: list = field(
        default_factory=list
    )

    discoveries: list = field(
        default_factory=list
    )

    experiences: list = field(
        default_factory=list
    )

    def add_observation(
        self,
        observation: Dict[str, Any],
    ):

        self.observations.append(
            dict(observation)
        )

    def add_discovery(
        self,
        discovery,
    ):

        self.discoveries.append(
            discovery
        )

    def add_experience(
        self,
        experience,
    ):

        self.experiences.append(
            experience
        )

    def latest_observation(self):

        if not self.observations:
            return None

        return self.observations[-1]

    def to_dict(self):

        return {
            "experiment_id":
                self.experiment_id,
            "target":
                self.target,
            "hypothesis":
                self.hypothesis,
            "metadata":
                dict(self.metadata),
            "baseline":
                self.baseline,
            "previous_experiences":
                len(
                    self.previous_experiences
                ),
            "observations":
                len(self.observations),
            "discoveries":
                len(self.discoveries),
            "experiences":
                len(self.experiences),
        }
