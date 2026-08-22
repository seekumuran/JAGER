import unittest

from .policy import SecurityPolicy


class TestSecurityPolicy(
    unittest.TestCase
):

    def setUp(self):

        self.policy = SecurityPolicy()

    def test_safe_action(self):

        result = self.policy.evaluate(
            {
                "type": "probe",
                "parameters": {},
            }
        )

        self.assertTrue(
            result.allowed
        )

    def test_credential_access(self):

        result = self.policy.evaluate(
            {
                "type": "probe",
                "parameters": {
                    "credential_access": True
                },
            }
        )

        self.assertFalse(
            result.allowed
        )

        self.assertEqual(
            result.risk,
            1.0,
        )

    def test_system_access(self):

        result = self.policy.evaluate(
            {
                "type": "probe",
                "parameters": {
                    "system_access": True
                },
            }
        )

        self.assertFalse(
            result.allowed
        )

    def test_exfiltration(self):

        result = self.policy.evaluate(
            {
                "type": "probe",
                "parameters": {
                    "network_exfiltration": True
                },
            }
        )

        self.assertFalse(
            result.allowed
        )

    def test_shell_execution(self):

        result = self.policy.evaluate(
            {
                "type": "action",
                "parameters": {
                    "operation":
                        "execute_shell"
                },
            }
        )

        self.assertFalse(
            result.allowed
        )

    def test_high_risk_action(self):

        result = self.policy.evaluate(
            {
                "type": "probe",
                "parameters": {
                    "high_resource_usage": True,
                    "privileged": True,
                },
            }
        )

        self.assertFalse(
            result.allowed
        )


if __name__ == "__main__":
    unittest.main()
