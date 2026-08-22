import unittest

from .target_metrics import TargetMetrics
from .baseline import BaselineBuilder
from .anomaly_detector import (
    AnomalyDetector,
)


class TestAnomalyDetector(
    unittest.TestCase
):

    def setUp(self):

        metrics = TargetMetrics()

        metrics.record(
            "blackbox",
            {
                "cpu_usage": 40.0,
                "latency_ms": 10.0,
            },
            1.0,
        )

        metrics.record(
            "blackbox",
            {
                "cpu_usage": 60.0,
                "latency_ms": 20.0,
            },
            2.0,
        )

        self.baseline = (
            BaselineBuilder().build(
                metrics,
                "blackbox",
            )
        )

    def test_normal_observation(self):

        detector = AnomalyDetector(
            threshold=2.0
        )

        anomalies = detector.detect(
            self.baseline,
            {
                "cpu_usage": 50.0,
                "latency_ms": 15.0,
            },
        )

        self.assertFalse(
            detector.is_anomalous(
                anomalies
            )
        )

    def test_anomalous_observation(self):

        detector = AnomalyDetector(
            threshold=1.5
        )

        anomalies = detector.detect(
            self.baseline,
            {
                "cpu_usage": 100.0,
                "latency_ms": 50.0,
            },
        )

        self.assertTrue(
            detector.is_anomalous(
                anomalies
            )
        )

    def test_anomaly_count(self):

        detector = AnomalyDetector(
            threshold=1.5
        )

        anomalies = detector.detect(
            self.baseline,
            {
                "cpu_usage": 100.0,
                "latency_ms": 50.0,
            },
        )

        self.assertEqual(
            detector.anomaly_count(
                anomalies
            ),
            2,
        )

    def test_insufficient_samples(self):

        metrics = TargetMetrics()

        metrics.record(
            "blackbox",
            {
                "cpu_usage": 50.0,
            },
            1.0,
        )

        baseline = (
            BaselineBuilder().build(
                metrics,
                "blackbox",
            )
        )

        detector = AnomalyDetector()

        anomalies = detector.detect(
            baseline,
            {
                "cpu_usage": 100.0,
            },
        )

        self.assertEqual(
            anomalies,
            {},
        )

    def test_unknown_metric(self):

        detector = AnomalyDetector()

        anomalies = detector.detect(
            self.baseline,
            {
                "unknown_metric": 999.0,
            },
        )

        self.assertNotIn(
            "unknown_metric",
            anomalies,
        )


if __name__ == "__main__":
    unittest.main()
