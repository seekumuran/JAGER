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

from ..runtime.experiment import (
    Experiment,
)

from ..runtime.experiment_runner import (
    ExperimentRunner,
)

from .jager_orchestrator import (
    JagerOrchestrator,
)


class TestJagerOrchestrator(
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

        self.orchestrator = (
            JagerOrchestrator(
                planner=
                    ExperimentPlanner(),
                runner=runner,
            )
        )

    def test_plan(self):

        goal = Goal.create(
            target="mock",
            objective=(
                "Understand target."
            ),
            constraints={
                "maximum_risk": 0.5
            },
        )

        plan = (
            self.orchestrator.plan(
                goal
            )
        )

        self.assertIsNotNone(
            plan["best"]
        )

    def test_execute_candidate(self):

        goal = Goal.create(
            target="mock",
            objective="Probe target",
            constraints={
                "maximum_risk": 0.5
            },
        )

        plan = (
            self.orchestrator.plan(
                goal
            )
        )

        candidate = plan["best"]

        experiment = Experiment.create(
            target="mock",
            hypothesis=
                candidate.hypothesis,
        )

        context, result = (
            self.orchestrator
            .execute_candidate(
                experiment,
                candidate,
                risk_level="low",
            )
        )

        self.assertEqual(
            result.experiment_id,
            experiment.experiment_id,
        )

        self.assertIn(
            result.status,
            {
                "success",
                "error",
            },
        )

        self.assertGreaterEqual(
            len(context.observations),
            1,
        )


if __name__ == "__main__":
    unittest.main()
