import unittest

from .result_validator import (
    ResultValidator,
)


class TestResultValidator(unittest.TestCase):

    def test_valid_result(self):
        result = {
            "run_id": "run-1",
            "seed": 42,
            "budget": 10,
            "experiments": [],
            "events": [],
            "discoveries": [],
        }

        self.assertTrue(
            ResultValidator().validate(
                result
            )
        )

    def test_missing_field(self):
        result = {
            "run_id": "run-1",
            "seed": 42,
            "budget": 10,
            "experiments": [],
            "events": [],
        }

        with self.assertRaises(
            ValueError
        ):
            ResultValidator().validate(
                result
            )


if __name__ == "__main__":
    unittest.main()
