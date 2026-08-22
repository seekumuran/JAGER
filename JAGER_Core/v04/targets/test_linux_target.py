import unittest

from .linux_target import (
    LinuxTarget,
)


class TestLinuxTarget(
    unittest.TestCase
):

    def setUp(self):
        self.target = LinuxTarget()

    def test_observe_structure(self):

        result = (
            self.target.observe()
        )

        self.assertIn(
            "inputs",
            result,
        )

        self.assertIn(
            "telemetry",
            result,
        )

        self.assertIn(
            "status",
            result,
        )

    def test_status_is_valid(self):

        result = (
            self.target.observe()
        )

        self.assertIn(
            result["status"],
            {
                "NORMAL",
                "DEGRADED",
                "FAILED",
            },
        )

    def test_cpu_range(self):

        result = (
            self.target.observe()
        )

        cpu = result[
            "telemetry"
        ]["cpu_usage"]

        self.assertGreaterEqual(
            cpu,
            0.0,
        )

        self.assertLessEqual(
            cpu,
            100.0,
        )

    def test_memory_range(self):

        result = (
            self.target.observe()
        )

        memory = result[
            "telemetry"
        ]["memory_usage"]

        self.assertGreaterEqual(
            memory,
            0.0,
        )

        self.assertLessEqual(
            memory,
            100.0,
        )

    def test_process_count(self):

        result = (
            self.target.observe()
        )

        processes = result[
            "telemetry"
        ]["process_count"]

        self.assertGreaterEqual(
            processes,
            0,
        )

    def test_thread_count(self):

        result = (
            self.target.observe()
        )

        threads = result[
            "telemetry"
        ]["thread_count"]

        self.assertGreaterEqual(
            threads,
            0,
        )


if __name__ == "__main__":
    unittest.main()
