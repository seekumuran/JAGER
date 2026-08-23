from typing import Optional

from ..config.config import JagerConfig

from ..persistence.persistent_state_manager import (
    PersistentStateManager,
)

from ..persistence.json_runtime_state_repository import (
    JsonRuntimeStateRepository,
)

from ..planner.goal import Goal

from ..planner.adaptive_planner import (
    AdaptivePlanner,
)

from .adaptive_loop import (
    AdaptiveLoop,
)

from .jager_orchestrator import (
    JagerOrchestrator,
)


class PersistentJagerRuntime:

    def __init__(
        self,
        orchestrator: JagerOrchestrator,
        config: Optional[
            JagerConfig
        ] = None,
        state_path: str = (
            "data/runtime_state.json"
        ),
    ):

        self.orchestrator = orchestrator

        self.config = (
            config or JagerConfig()
        )

        self.config.validate()

        repository = (
            JsonRuntimeStateRepository(
                state_path
            )
        )

        self.state = (
            PersistentStateManager(
                repository
            )
        )

        self.adaptive_planner = (
            AdaptivePlanner()
        )

        self.loop = AdaptiveLoop(
            orchestrator=
                orchestrator,
            planner=
                self.adaptive_planner,
        )

    def run(
        self,
        goal: Goal,
        maximum_iterations: Optional[
            int
        ] = None,
    ):

        iterations = (
            maximum_iterations
            if maximum_iterations is not None
            else self.config.max_iterations
        )

        self.state.event(
            "runtime_started",
            {
                "target": goal.target,
                "objective":
                    goal.objective,
            },
        )

        result = None

        try:

            result = self.loop.run(
                goal=goal,
                maximum_iterations=
                    iterations,
            )

            for item in result[
                "history"
            ]:

                orchestration_result = (
                    item["result"]
                )

                experiment_id = (
                    orchestration_result
                    .experiment_id
                )

                self.state.begin(
                    experiment_id
                )

                if (
                    orchestration_result
                    .succeeded()
                ):

                    self.state.complete(
                        experiment_id
                    )

                else:

                    self.state.fail(
                        experiment_id
                    )

                if (
                    orchestration_result
                    .discovery is not None
                ):

                    self.state.discovery_found()

                if (
                    orchestration_result
                    .experience is not None
                ):

                    self.state.experience_created()

            self.state.event(
                "runtime_completed",
                {
                    "iterations":
                        result[
                            "iterations"
                        ],
                },
            )

            return result

        except Exception as exc:

            self.state.event(
                "runtime_failed",
                {
                    "error":
                        str(exc),
                },
            )

            raise

    def snapshot(self):

        return self.state.snapshot()

    def reset(self):

        self.state.reset()
