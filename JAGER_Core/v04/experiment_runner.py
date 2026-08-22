import time
import uuid

from .experiment_context import (
    ExperimentContext,
)


class ExperimentRunner:

    def __init__(
        self,
        target_manager,
        reward_function=None,
    ):
        self.target_manager = (
            target_manager
        )

        self.reward_function = (
            reward_function
        )

        self.history = []

    def execute(
        self,
        action,
    ):

        target = (
            self.target_manager.current()
        )

        experiment_id = (
            f"exp-{uuid.uuid4().hex[:12]}"
        )

        context = ExperimentContext(
            experiment_id=experiment_id,
            target_name=target.name,
            action=action,
        )

        started = time.perf_counter()

        observation = (
            self.target_manager.observe(
                **action.get(
                    "parameters",
                    {},
                )
            )
        )

        elapsed_ms = (
            time.perf_counter() - started
        ) * 1000.0

        context.record_observation(
            observation
        )

        context.reward = (
            self._calculate_reward(
                observation
            )
        )

        context.novelty = (
            self._calculate_novelty(
                observation
            )
        )

        self.history.append(
            context
        )

        return {
            **context.to_dict(),
            "latency_ms": elapsed_ms,
        }

    def _calculate_reward(
        self,
        observation,
    ):

        if self.reward_function:

            return float(
                self.reward_function(
                    observation
                )
            )

        status = observation.get(
            "status"
        )

        if status == "FAILED":
            return 1.0

        if status == "DEGRADED":
            return 0.5

        return 0.0

    def _calculate_novelty(
        self,
        observation,
    ):

        if not self.history:
            return 1.0

        current = observation.get(
            "telemetry",
            {},
        )

        previous = [
            item.observation.get(
                "telemetry",
                {},
            )
            for item in self.history
        ]

        if not previous:
            return 1.0

        matches = 0

        for telemetry in previous:

            if telemetry == current:
                matches += 1

        return (
            1.0
            if matches == 0
            else 0.0
        )
