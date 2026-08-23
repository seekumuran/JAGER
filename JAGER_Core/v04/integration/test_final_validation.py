import unittest

from .final_validation import (
    run_final_validation,
)


class TestFinalValidation(
    unittest.TestCase
):

    def test_validation_structure(self):

        report = (
            run_final_validation()
        )

        self.assertIn(
            "audit",
            report,
        )

        self.assertIn(
            "imports",
            report,
        )

        self.assertIn(
            "tests",
            report,
        )

        self.assertIn(
            "healthy",
            report,
        )


if __name__ == "__main__":
    unittest.main()
