import unittest

from .action_schema import (
    ActionSchema,
)


class TestActionSchema(
    unittest.TestCase
):

    def setUp(self):

        self.schema = ActionSchema()

    def test_valid_linux_action(self):

        result = self.schema.validate(
            "linux",
            {
                "type": "probe",
                "parameters": {
                    "operation": "observe",
                },
            },
        )

        self.assertTrue(
            result.valid
        )

    def test_valid_ai_action(self):

        result = self.schema.validate(
            "ai_sandbox",
            {
                "type": "probe",
                "parameters": {
                    "operation":
                        "prompt_observation",
                    "prompt":
                        "hello",
                },
            },
        )

        self.assertTrue(
            result.valid
        )

    def test_invalid_operation(self):

        result = self.schema.validate(
            "linux",
            {
                "type": "probe",
                "parameters": {
                    "operation":
                        "execute_shell",
                },
            },
        )

        self.assertFalse(
            result.valid
        )

    def test_unknown_target(self):

        result = self.schema.validate(
            "unknown",
            {
                "type": "probe",
                "parameters": {},
            },
        )

        self.assertFalse(
            result.valid
        )

    def test_invalid_parameters(self):

        result = self.schema.validate(
            "linux",
            {
                "type": "probe",
                "parameters": "invalid",
            },
        )

        self.assertFalse(
            result.valid
        )

    def test_operations(self):

        operations = (
            self.schema.operations_for(
                "linux"
            )
        )

        self.assertIn(
            "observe",
            operations,
        )


if __name__ == "__main__":
    unittest.main()
