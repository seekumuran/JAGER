from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class IterationContext:

    experiment_id: str

    iteration: int

    target: str

    objective: str

    state: Dict[str, Any] = field(
        default_factory=dict
    )

    observations: list = field(
        default_factory=list
    )

    actions: list = field(
        default_factory=list
    )

    discoveries: list = field(
        default_factory=list
    )

    errors: list = field(
        default_factory=list
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    def record_observation(
        self,
        observation: Any,
    ):
        self.observations.append(
            observation
        )

    def record_action(
        self,
        action: Any,
    ):
        self.actions.append(
            action
        )

    def record_discovery(
        self,
        discovery: Any,
    ):
        self.discoveries.append(
            discovery
        )

    def record_error(
        self,
        error: Exception | str,
    ):
        self.errors.append(
            str(error)
        )

    def update_state(
        self,
        values: Dict[str, Any],
    ):
        self.state.update(values)

    def set_metadata(
        self,
        key: str,
        value: Any,
    ):
        self.metadata[key] = value

    def to_dict(self):

        return {
            "experiment_id":
                self.experiment_id,
            "iteration":
                self.iteration,
            "target":
                self.target,
            "objective":
                self.objective,
            "state":
                dict(self.state),
            "observations":
                list(self.observations),
            "actions":
                list(self.actions),
            "discoveries":
                list(self.discoveries),
            "errors":
                list(self.errors),
            "metadata":
                dict(self.metadata),
        }
