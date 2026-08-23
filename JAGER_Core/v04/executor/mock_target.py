from typing import Any, Dict

from .target import Target


class MockTarget(Target):

    def __init__(
        self,
        target_name: str = "mock",
    ):

        self._name = target_name

        self.execution_count = 0

        self.observation_count = 0

        self.state: Dict[str, Any] = {
            "status": "ready",
            "executions": 0,
        }

    @property
    def name(self):

        return self._name

    def observe(self):

        self.observation_count += 1

        return {
            "target": self.name,
            "state": dict(self.state),
            "observation_count":
                self.observation_count,
        }

    def execute(
        self,
        action_type,
        parameters,
    ):

        self.execution_count += 1

        self.state[
            "executions"
        ] = self.execution_count

        if action_type == "probe":

            return {
                "action": action_type,
                "parameters":
                    dict(parameters),
                "execution":
                    self.execution_count,
            }

        if action_type == "observe":

            return self.observe()

        if action_type == "set_state":

            key = parameters.get(
                "key"
            )

            if key is None:
                raise ValueError(
                    "set_state requires "
                    "'key'"
                )

            self.state[key] = (
                parameters.get("value")
            )

            return {
                "updated": key,
                "value":
                    self.state[key],
            }

        raise ValueError(
            f"Unsupported action: "
            f"{action_type}"
        )
