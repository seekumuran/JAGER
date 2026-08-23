from typing import Any, Dict

from .target_adapter import (
    TargetAdapter,
)


class MockTargetAdapter(
    TargetAdapter
):

    def __init__(
        self,
        target_name: str = "mock",
    ):

        if not target_name:
            raise ValueError(
                "target_name cannot be empty"
            )

        self._name = target_name

    @property
    def name(self):

        return self._name

    def execute(
        self,
        action_type: str,
        parameters: Dict[str, Any],
    ):

        parameters = dict(
            parameters or {}
        )

        return {
            "status": "success",
            "target": self.name,
            "action_type": action_type,
            "parameters": parameters,
            "observation": {
                "state": "observed",
            },
        }
