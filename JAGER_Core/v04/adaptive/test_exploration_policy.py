import unittest

from .exploration_policy import (
    ExplorationPolicy,
)


class TestExplorationPolicy(
    unittest.TestCase
):

    def test_initial_rate(self):

        policy = ExplorationPolicy(
            initial_rate=0.5,
            minimum_rate=0.1,
            maximum_rate=0.8,
        )

        self.assertAlmostEqual(
            policy.rate,
            0.5,
        )

    def test_rate_decays(self):

        policy = ExplorationPolicy(
            initial_rate=0.8,
            minimum_rate=0.1,
            maximum_rate=0.8,
            decay=0.5,
        )

        first = policy.rate

        for _ in range(10):
            policy.next_step()

        second = policy.rate

        self.assertLess(
            second,
            first,
        )

    def test_minimum_rate(self):

        policy = ExplorationPolicy(
            initial_rate=0.5,
            minimum_rate=0.2,
            maximum_rate=0.8,
            decay=10.0,
        )

        for _ in range(100):
            policy.next_step()

        self.assertEqual(
            policy.rate,
            0.2,
        )

    def test_statistics(self):

        policy = ExplorationPolicy()

        policy.observe_candidates(20)
        policy.observe_selection(5)
        policy.observe_discovery(True)

        snapshot = policy.snapshot()

        self.assertEqual(
            snapshot["total_candidates"],
            20,
        )

        self.assertEqual(
            snapshot["selected_candidates"],
            5,
        )

        self.assertEqual(
            snapshot["discoveries"],
            1,
        )

        self.assertEqual(
            snapshot["discovery_rate"],
            0.2,
        )


if __name__ == "__main__":
    unittest.main()
