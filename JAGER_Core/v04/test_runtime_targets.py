import unittest

from .config import JagerConfig
from .integration import JagerRuntime
from .runtime_targets import (
    register_default_targets,
)


class TestRuntimeTargets(
    unittest.TestCase
):

    def test_default_targets(self):

        runtime = JagerRuntime(
            config=JagerConfig(
                seed=42,
                budget=5,
            )
        )

        register_default_targets(
            runtime
        )

        targets = (
            runtime.available_targets()
        )

        self.assertIn(
            "blackbox",
            targets,
        )

        self.assertIn(
            "linux",
            targets,
        )

        self.assertIn(
            "ai_sandbox",
            targets,
        )

    def test_select_linux(self):

        runtime = JagerRuntime(
            config=JagerConfig(
                seed=42,
                budget=5,
            )
        )

        register_default_targets(
            runtime
        )

        target = runtime.select_target(
            "linux"
        )

        self.assertEqual(
            target.name,
            "linux",
        )

    def test_select_ai_sandbox(self):

        runtime = JagerRuntime(
            config=JagerConfig(
                seed=42,
                budget=5,
            )
        )

        register_default_targets(
            runtime
        )

        target = runtime.select_target(
            "ai_sandbox"
        )

        self.assertEqual(
            target.name,
            "ai_sandbox",
        )


if __name__ == "__main__":
    unittest.main()
