from typing import Any, Dict

from ..api.jager import Jager
from ..executor.mock_target_adapter import (
    MockTargetAdapter,
)
from ..executor.target_registry import (
    TargetRegistry,
)

from .system_health import (
    SystemHealth,
)


class EndToEndRunner:

    def __init__(
        self,
        jager: Jager,
    ):

        self.jager = jager

    def health_check(self):

        return SystemHealth(
            self.jager
        ).check()

    def run(
        self,
        target: str,
        objective: str,
        maximum_iterations: int = 1,
    ) -> Dict[str, Any]:

        health = self.health_check()

        if not health["healthy"]:

            raise RuntimeError(
                "JÄGER health check failed"
            )

        result = self.jager.run(
            target=target,
            objective=objective,
            maximum_iterations=
                maximum_iterations,
        )

        return {
            "success": True,
            "result": result,
            "runtime":
                self.jager.status(),
        }


def build_mock_runtime():

    registry = TargetRegistry()

    registry.register(
        MockTargetAdapter("mock")
    )

    return Jager(
        registry=registry
    )
