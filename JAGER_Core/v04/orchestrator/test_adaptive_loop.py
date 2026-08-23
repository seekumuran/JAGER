import unittest

from ..executor.executor import (
    ExperimentExecutor,
)

from ..executor.mock_target import (
    MockTarget,
)

from ..executor.registry import (
    TargetRegistry,
)

from ..planner.adaptive_planner import (
    AdaptivePlanner,
)

from ..planner.goal import (
    Goal,
)

from ..planner.planner import (
    ExperimentPlanner,
)

from ..policy.default_policy import (
    build_default_policy,
)

from ..policy.policy_mediator import (
    PolicyMediator,
)

from ..runtime.experiment_runner import (
    ExperimentRunner,
)

from .adaptive_loop import (
    AdaptiveLoop,
)

from .jager_orchestrator import (
    JagerOrchestrator,
)


class TestAdaptiveLoop(
    unittest.TestCase
):

    def setUp(self):

        registry = TargetRegistry()

        registry.register(
            MockTarget("mock")
        )

        executor = ExperimentExecutor(
            registry
        )

        policy = PolicyMediator(
            build_default_policy()
        )

        runner = ExperimentRunner(
            executor=executor,
            policy=policy,
        )

        orchestrator = (
            JagerOrchestrator(
                planner=
                    ExperimentPlanner(),
                runner=runner,
            )
        )

        self.loop = AdaptiveLoop(
            orchestrator=orchestrator,
            planner=AdaptivePlanner(),
        )

    def test_loop_runs(self):

        goal = Goal.create(
            target="mock",
            objective=(
                "Explore target behavior."
            ),
            constraints={
                "maximum_risk": 0.5
            },
        )

        result = self.loop.run(
            goal,
            maximum_iterations=2,
        )

        self.assertGreater(
            result["iterations"],
            0,
        )

        self.assertEqual(
            len(result["history"]),
            result["iterations"],
        )

        self.assertIsNotNone(
            result["final_plan"]
        )


if __name__ == "__main__":
    unittest.main()
