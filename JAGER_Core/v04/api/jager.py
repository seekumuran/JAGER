from typing import Any, Dict, Optional

from ..config.config import JagerConfig
from ..config.defaults import default_config

from ..executor.registry import TargetRegistry

from ..orchestrator.runtime_factory import (
    build_runtime,
)

from ..planner.goal import Goal


class Jager:

    def __init__(
        self,
        registry: TargetRegistry,
        config: Optional[
            JagerConfig
        ] = None,
        state_path: str = (
            "data/runtime_state.json"
        ),
    ):

        self.config = (
            config
            or default_config()
        )

        self.config.validate()

        self.registry = registry

        self.runtime = build_runtime(
            registry=registry,
            config=self.config,
            state_path=state_path,
        )

    def run(
        self,
        target: str,
        objective: str,
        constraints: Optional[
            Dict[str, Any]
        ] = None,
        success_criteria=None,
        priority: float = 0.5,
        maximum_iterations: Optional[
            int
        ] = None,
    ):

        if not self.registry.get(
            target
        ):

            raise ValueError(
                f"Unknown target: {target}"
            )

        goal = Goal.create(
            target=target,
            objective=objective,
            constraints=(
                constraints or {}
            ),
            success_criteria=(
                success_criteria or []
            ),
            priority=priority,
        )

        return self.runtime.run(
            goal=goal,
            maximum_iterations=
                maximum_iterations,
        )

    def status(self):

        return self.runtime.snapshot()

    def reset(self):

        self.runtime.reset()

    def targets(self):

        return self.registry.names()
