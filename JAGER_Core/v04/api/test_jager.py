import tempfile
import unittest
from pathlib import Path

from ..executor.mock_target import (
    MockTarget,
)

from ..executor.registry import (
    TargetRegistry,
)

from .jager import (
    Jager,
)


class TestJagerAPI(
    unittest.TestCase
):

    def test_public_api(self):

        with tempfile.TemporaryDirectory() as tmp:

            registry = TargetRegistry()

            registry.register(
                MockTarget("mock")
            )

            jager = Jager(
                registry=registry,
                state_path=str(
                    Path(tmp)
                    / "state.json"
                ),
            )

            result = jager.run(
                target="mock",
                objective=(
                    "Explore target behavior."
                ),
                constraints={
                    "maximum_risk": 0.5
                },
                maximum_iterations=1,
            )

            self.assertGreaterEqual(
                result["iterations"],
                1,
            )

            self.assertIn(
                "history",
                result,
            )

    def test_unknown_target(self):

        registry = TargetRegistry()

        jager = Jager(
            registry=registry
        )

        with self.assertRaises(
            ValueError
        ):

            jager.run(
                target="does-not-exist",
                objective="Test",
            )

    def test_status(self):

        registry = TargetRegistry()

        registry.register(
            MockTarget("mock")
        )

        jager = Jager(
            registry=registry
        )

        status = jager.status()

        self.assertEqual(
            status["status"],
            "idle",
        )

    def test_targets(self):

        registry = TargetRegistry()

        registry.register(
            MockTarget("mock")
        )

        jager = Jager(
            registry=registry
        )

        self.assertIn(
            "mock",
            jager.targets(),
        )


if __name__ == "__main__":
    unittest.main()
