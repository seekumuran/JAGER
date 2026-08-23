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

from ..policy.default_policy import (
    build_default_policy,
)

from ..policy.policy_mediator import (
    PolicyMediator,
)

from .runtime import (
    JagerRuntime,
)


class TestJagerRuntime(
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

        self.runtime = JagerRuntime(
            executor=executor,
            policy=policy,
        )

    def test_allowed_experiment(self):

        experiment = (
            self.runtime.create_experiment(
                target="mock",
                hypothesis=(
                    "Low-risk probing "
                    "reveals target state."
                ),
            )
        )

        result = self.runtime.run(
            experiment,
            action_type="probe",
            parameters={
                "load": 50
            },
            risk_level="low",
        )

        self.assertTrue(
            result["allowed"]
        )

        self.assertEqual(
            experiment.status,
            "completed",
        )

        chain = self.runtime.evidence(
            experiment.experiment_id
        )

        self.assertTrue(
            chain.backbone_complete()
        )

    def test_denied_experiment(self):

        experiment = (
            self.runtime.create_experiment(
                target="mock",
                hypothesis=(
                    "Unknown-risk action "
                    "should be blocked."
                ),
            )
        )

        result = self.runtime.run(
            experiment,
            action_type="probe",
            risk_level="unknown",
        )

        self.assertFalse(
            result["allowed"]
        )

        self.assertEqual(
            experiment.status,
            "failed",
        )

        chain = self.runtime.evidence(
            experiment.experiment_id
        )

        self.assertFalse(
            chain.backbone_complete()
        )

        self.assertIn(
            "action",
            chain.missing(),
        )

    def test_runtime_snapshot(self):

        experiment = (
            self.runtime.create_experiment(
                target="mock",
                hypothesis="observe state",
            )
        )

        self.assertIsNotNone(
            self.runtime.get_experiment(
                experiment.experiment_id
            )
        )

        snapshot = (
            self.runtime.snapshot()
        )

        self.assertEqual(
            len(snapshot["experiments"]),
            1,
        )


if __name__ == "__main__":
    unittest.main()
