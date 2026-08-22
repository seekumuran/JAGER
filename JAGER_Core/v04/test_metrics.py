import unittest

from .experiment_metrics import (
    ExperimentMetrics,
)


class TestExperimentMetrics(unittest.TestCase):

    def test_metrics(self):
        metrics = ExperimentMetrics()

        metrics.record_action()
        metrics.record_action()
        metrics.record_failure()
        metrics.record_reward(10)
        metrics.record_reward(20)

        summary = metrics.summary()

        self.assertEqual(
            summary["counters"]["actions"],
            2,
        )

        self.assertEqual(
            summary["counters"]["failures"],
            1,
        )

        self.assertEqual(
            summary["averages"]["reward"],
            15.0,
        )


if __name__ == "__main__":
    unittest.main()
