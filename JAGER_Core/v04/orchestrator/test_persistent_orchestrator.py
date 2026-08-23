import tempfile
import unittest
from pathlib import Path

from ..config.defaults import (
    default_config,
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

from .runtime_factory import (
    build_runtime,
)


class TestPersistentRuntime(
    unittest.TestCase
):

    def test_runtime_persists_state(self):

        with tempfile.TemporaryDirectory() as tmp:

            registry = TargetRegistry()

            registry.register(
                MockTarget("mock")
            )

            state_path = str(
                Path(tmp)
                / "runtime.json"
            )

            config = default_config()

            config.max_iterations = 1

            runtime = build_runtime(
                registry=registry,
                config=config,
                state_path=state_path,
            )

            goal = Goal.create(
                target="mock",
                objective=(
                    "Explore target."
                ),
                constraints={
                    "maximum_risk": 0.5
                },
            )

            result = runtime.run(
                goal
            )

            self.assertGreaterEqual(
                result["iterations"],
                1,
            )

            snapshot = (
                runtime.snapshot()
            )

            self.assertGreater(
                snapshot[
                    "experiments_completed"
                ],
                0,
            )

            self.assertTrue(
                Path(state_path).exists()
            )


if __name__ == "__main__":
    unittest.main()
