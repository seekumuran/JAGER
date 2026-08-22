import unittest

from .ai_sandbox import AISandbox


class TestAISandbox(
    unittest.TestCase
):

    def setUp(self):
        self.sandbox = AISandbox(
            seed=42
        )

    def test_safe_operation_allowed(self):

        result = self.sandbox.execute(
            "summarize",
            {
                "text": "synthetic"
            },
        )

        self.assertEqual(
            result["decision"],
            "ALLOW",
        )

    def test_unknown_operation_denied(self):

        result = self.sandbox.execute(
            "execute_shell",
            {
                "command": "id"
            },
        )

        self.assertEqual(
            result["decision"],
            "DENY",
        )

    def test_credential_access_denied(self):

        result = self.sandbox.execute(
            "read_context",
            {
                "credential_access": True
            },
        )

        self.assertEqual(
            result["decision"],
            "DENY",
        )

    def test_network_exfiltration_denied(self):

        result = self.sandbox.execute(
            "generate",
            {
                "network_exfiltration": True
            },
        )

        self.assertEqual(
            result["decision"],
            "DENY",
        )

    def test_observation(self):

        self.sandbox.execute(
            "summarize",
            {},
        )

        self.sandbox.execute(
            "execute_shell",
            {},
        )

        result = self.sandbox.observe()

        self.assertEqual(
            result["telemetry"][
                "action_count"
            ],
            2,
        )

        self.assertEqual(
            result["telemetry"][
                "allowed_actions"
            ],
            1,
        )

        self.assertEqual(
            result["telemetry"][
                "denied_actions"
            ],
            1,
        )


if __name__ == "__main__":
    unittest.main()
