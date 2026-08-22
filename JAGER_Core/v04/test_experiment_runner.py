import unittest

from .action_generator import (
    ActionGenerator,
)

from .experiment_runner import (
    ExperimentRunner,
)

from .target_manager import (
    TargetManager,
)

from .targets.linux_target import (
    LinuxTarget,
)


class TestExperimentRunner(
    unittest.TestCase
):

    def test_linux_experiment(self):

        manager = TargetManager()

        manager.register(
            LinuxTarget()
        )

        manager.select(
            "linux"
        )

        runner = ExperimentRunner(
            manager
        )

        generator = ActionGenerator(
            seed=42
        )

        action = generator.generate(
            "linux"
        )

        result = runner.execute(
            action
        )

        self.assertIn(
            "experiment_id",
            result,
        )

        self.assertIn(
            "observation",
            result,
        )

        self.assertIn(
            "reward",
            result,
        )

        self.assertIn(
            "novelty",
            result,
        )

        self.assertIn(
            result["observation"][
                "status"
            ],
            {
                "NORMAL",
                "DEGRADED",
                "FAILED",
            },
        )

    def test_history(self):

        manager = TargetManager()

        manager.register(
            LinuxTarget()
        )

        manager.select(
            "linux"
        )

        runner = ExperimentRunner(
            manager
        )

        action = {
            "type": "observe",
            "parameters": {},
        }

        runner.execute(action)
        runner.execute(action)

        self.assertEqual(
            len(runner.history),
            2,
        )


if __name__ == "__main__":
    unittest.main()
