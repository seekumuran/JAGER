import unittest

from .hunter import JagerHunter
from .hunter_factory import (
    HunterCandidateFactory,
)
from .integration import JagerRuntime
from .config import JagerConfig
from .runtime_targets import (
    register_default_targets,
)


class TestJagerHunter(
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

        self.runtime.select_target(
            "blackbox"
        )

        self.factory = (
            HunterCandidateFactory(
                target_name="blackbox",
                seed=42,
                candidate_count=5,
            )
        )

    def test_single_step(self):

        hunter = JagerHunter(
            self.runtime,
            self.factory,
        )

        result = hunter.step()

        self.assertIn(
            "experiment_id",
            result,
        )

        self.assertEqual(
            len(hunter.results),
            1,
        )

    def test_multiple_steps(self):

        hunter = JagerHunter(
            self.runtime,
            self.factory,
        )

        results = list(
            hunter.run(5)
        )

        self.assertEqual(
            len(results),
            5,
        )

        self.assertEqual(
            len(hunter.results),
            5,
        )

    def test_running_state(self):

        hunter = JagerHunter(
            self.runtime,
            self.factory,
        )

        self.assertFalse(
            hunter.running
        )

        list(hunter.run(1))

        self.assertFalse(
            hunter.running
        )

    def test_summary(self):

        hunter = JagerHunter(
            self.runtime,
            self.factory,
        )

        list(hunter.run(5))

        summary = hunter.summary()

        self.assertEqual(
            summary["experiments"],
            5,
        )

        self.assertIn(
            "average_reward",
            summary,
        )

    def test_invalid_steps(self):

        hunter = JagerHunter(
            self.runtime,
            self.factory,
        )

        with self.assertRaises(
            ValueError
        ):
            list(hunter.run(0))


if __name__ == "__main__":
    unittest.main()
