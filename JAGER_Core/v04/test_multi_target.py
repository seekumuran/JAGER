import unittest

from .config import JagerConfig
from .integration import JagerRuntime
from .multi_target import (
    MultiTargetRunner,
)
from .runtime_targets import (
    register_default_targets,
)


class TestMultiTargetRunner(
    unittest.TestCase
):

    def setUp(self):

        self.runtime = JagerRuntime(
            config=JagerConfig(
                seed=42,
                budget=20,
            )
        )

        register_default_targets(
            self.runtime
        )

    def test_multiple_targets(self):

        runner = MultiTargetRunner(
            runtime=self.runtime,
            targets=[
                "linux",
                "ai_sandbox",
                "blackbox",
            ],
            steps_per_target=2,
            candidate_count=3,
        )

        results = runner.run()

        self.assertEqual(
            set(results.keys()),
            {
                "linux",
                "ai_sandbox",
                "blackbox",
            },
        )

        self.assertEqual(
            len(results["linux"]),
            2,
        )

        self.assertEqual(
            len(results["ai_sandbox"]),
            2,
        )

        self.assertEqual(
            len(results["blackbox"]),
            2,
        )

    def test_summary(self):

        runner = MultiTargetRunner(
            runtime=self.runtime,
            targets=[
                "linux",
                "blackbox",
            ],
            steps_per_target=2,
        )

        runner.run()

        summary = runner.summary()

        self.assertIn(
            "linux",
            summary,
        )

        self.assertIn(
            "blackbox",
            summary,
        )

        self.assertEqual(
            summary["linux"]["experiments"],
            2,
        )


if __name__ == "__main__":
    unittest.main()
