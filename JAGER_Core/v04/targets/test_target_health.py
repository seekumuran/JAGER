import unittest

from .target_health import (
    TargetHealthMonitor,
)


class TestTargetHealthMonitor(
    unittest.TestCase
):

    def test_health_record(self):

        monitor = (
            TargetHealthMonitor()
        )

        record = monitor.record(
            target="linux",
            available=True,
            latency_ms=2.5,
            details={
                "platform": "Linux"
            },
        )

        self.assertEqual(
            record.target,
            "linux",
        )

        self.assertTrue(
            monitor.healthy(
                "linux"
            )
        )

    def test_unavailable_target(self):

        monitor = (
            TargetHealthMonitor()
        )

        monitor.record(
            target="ai_sandbox",
            available=False,
            latency_ms=0.0,
        )

        self.assertFalse(
            monitor.healthy(
                "ai_sandbox"
            )
        )

    def test_snapshot(self):

        monitor = (
            TargetHealthMonitor()
        )

        monitor.record(
            "linux",
            True,
            1.0,
        )

        snapshot = (
            monitor.snapshot()
        )

        self.assertIn(
            "linux",
            snapshot,
        )


if __name__ == "__main__":
    unittest.main()
