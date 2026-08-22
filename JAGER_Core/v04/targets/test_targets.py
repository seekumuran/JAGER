import unittest

from .linux_target import (
    LinuxTarget,
)

from .ai_sandbox_target import (
    AISandboxTarget,
)


class TestLinuxTarget(
    unittest.TestCase
):

    def setUp(self):

        self.target = LinuxTarget()

    def test_capabilities(self):

        capabilities = (
            self.target.capabilities()
        )

        self.assertIn(
            "cpu_observation",
            capabilities,
        )

    def test_observation(self):

        result = self.target.observe(
            {
                "type": "probe",
                "parameters": {
                    "operation":
                        "observe",
                },
            }
        )

        self.assertEqual(
            result.target,
            "linux",
        )

        self.assertIn(
            result.status,
            {
                "NORMAL",
                "DEGRADED",
                "FAILED",
            },
        )

        self.assertIn(
            "process_count",
            result.telemetry,
        )


class TestAISandboxTarget(
    unittest.TestCase
):

    def setUp(self):

        self.target = (
            AISandboxTarget()
        )

    def test_prompt_observation(self):

        result = self.target.observe(
            {
                "type": "probe",
                "parameters": {
                    "prompt":
                        "hello jager",
                },
            }
        )

        self.assertEqual(
            result.status,
            "NORMAL",
        )

        self.assertEqual(
            result.telemetry[
                "prompt_length"
            ],
            11,
        )

    def test_prompt_limit(self):

        result = self.target.observe(
            {
                "type": "probe",
                "parameters": {
                    "prompt":
                        "x" * 5000,
                },
            }
        )

        self.assertEqual(
            result.status,
            "DENIED",
        )

    def test_request_counter(self):

        action = {
            "type": "probe",
            "parameters": {
                "prompt": "test",
            },
        }

        self.target.observe(action)
        result = self.target.observe(
            action
        )

        self.assertEqual(
            result.telemetry[
                "request_count"
            ],
            2,
        )


if __name__ == "__main__":
    unittest.main()
