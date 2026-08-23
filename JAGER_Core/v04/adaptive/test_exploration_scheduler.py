import unittest

from .exploration_scheduler import (
    ExplorationScheduler,
)


class TestExplorationScheduler(
    unittest.TestCase
):

    def test_allocation(self):

        scheduler = (
            ExplorationScheduler()
        )

        result = scheduler.allocate(
            budget=100,
            exploration_rate=0.3,
        )

        self.assertEqual(
            result.exploration,
            30,
        )

        self.assertEqual(
            result.exploitation,
            70,
        )

    def test_minimum_exploration(self):

        scheduler = (
            ExplorationScheduler(
                minimum_exploration=2
            )
        )

        result = scheduler.allocate(
            budget=10,
            exploration_rate=0.01,
        )

        self.assertEqual(
            result.exploration,
            2,
        )

        self.assertEqual(
            result.total,
            10,
        )

    def test_zero_budget(self):

        scheduler = (
            ExplorationScheduler()
        )

        result = scheduler.allocate(
            0,
            0.5,
        )

        self.assertEqual(
            result.total,
            0,
        )


if __name__ == "__main__":
    unittest.main()
