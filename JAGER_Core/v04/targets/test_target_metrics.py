import unittest

from .target_metrics import (
    TargetMetrics,
)


class TestTargetMetrics(
    unittest.TestCase
):

    def test_record_numeric_metrics(self):

        metrics = TargetMetrics()

        metrics.record(
            target="linux",
            telemetry={
                "cpu": 42.0,
                "processes": 10,
                "healthy": True,
                "name": "linux",
            },
            timestamp=1.0,
            experiment_id="exp-1",
        )

        self.assertEqual(
            metrics.count(
                "linux",
                "cpu",
            ),
            1,
        )

        self.assertEqual(
            metrics.latest(
                "linux",
                "cpu",
            ),
            42.0,
        )

    def test_summary(self):

        metrics = TargetMetrics()

        for index, value in enumerate(
            [10.0, 20.0, 30.0]
        ):

            metrics.record(
                "linux",
                {"cpu": value},
                float(index),
            )

        summary = metrics.summary(
            "linux",
            "cpu",
        )

        self.assertEqual(
            summary["count"],
            3,
        )

        self.assertEqual(
            summary["mean"],
            20.0,
        )

        self.assertEqual(
            summary["minimum"],
            10.0,
        )

        self.assertEqual(
            summary["maximum"],
            30.0,
        )

    def test_missing_metric(self):

        metrics = TargetMetrics()

        self.assertIsNone(
            metrics.latest(
                "linux",
                "cpu",
            )
        )

        self.assertEqual(
            metrics.summary(
                "linux",
                "cpu",
            )["count"],
            0,
        )

    def test_target_summary(self):

        metrics = TargetMetrics()

        metrics.record(
            "linux",
            {
                "cpu": 50.0,
                "memory": 70.0,
            },
            1.0,
        )

        result = metrics.target_summary(
            "linux"
        )

        self.assertIn(
            "cpu",
            result,
        )

        self.assertIn(
            "memory",
            result,
        )


if __name__ == "__main__":
    unittest.main()
