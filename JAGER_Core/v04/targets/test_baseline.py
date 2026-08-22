import unittest

from .target_metrics import (
    TargetMetrics,
)

from .baseline import (
    BaselineBuilder,
    BaselineComparator,
)


class TestBaseline(
    unittest.TestCase
):

    def setUp(self):

        self.metrics = TargetMetrics()

        self.metrics.record(
            "blackbox",
            {
                "cpu_usage": 40.0,
                "latency_ms": 10.0,
            },
            1.0,
        )

        self.metrics.record(
            "blackbox",
            {
                "cpu_usage": 60.0,
                "latency_ms": 20.0,
            },
            2.0,
        )

    def test_build(self):

        baseline = (
            BaselineBuilder().build(
                self.metrics,
                "blackbox",
            )
        )

        self.assertEqual(
            baseline.target,
            "blackbox",
        )

        self.assertEqual(
            baseline.samples,
            2,
        )

        self.assertEqual(
            baseline.metrics[
                "cpu_usage"
            ]["mean"],
            50.0,
        )

    def test_compare(self):

        baseline = (
            BaselineBuilder().build(
                self.metrics,
                "blackbox",
            )
        )

        result = (
            BaselineComparator().compare(
                baseline,
                {
                    "cpu_usage": 70.0,
                    "latency_ms": 25.0,
                },
            )
        )

        self.assertEqual(
            result["cpu_usage"]["delta"],
            20.0,
        )

        self.assertEqual(
            result["latency_ms"]["delta"],
            10.0,
        )


if __name__ == "__main__":
    unittest.main()
