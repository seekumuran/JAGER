import unittest

from .final_audit import (
    FinalAudit,
)


class TestFinalAudit(
    unittest.TestCase
):

    def test_all_checks_pass(self):

        audit = FinalAudit()

        audit.register(
            "first",
            lambda: True,
        )

        audit.register(
            "second",
            lambda: True,
        )

        self.assertTrue(
            audit.passed()
        )

        summary = (
            audit.summary()
        )

        self.assertEqual(
            summary["passed"],
            2,
        )

        self.assertEqual(
            summary["failed"],
            0,
        )

    def test_failed_check(self):

        audit = FinalAudit()

        audit.register(
            "good",
            lambda: True,
        )

        audit.register(
            "bad",
            lambda: False,
        )

        self.assertFalse(
            audit.passed()
        )

        summary = (
            audit.summary()
        )

        self.assertEqual(
            summary["passed"],
            1,
        )

        self.assertEqual(
            summary["failed"],
            1,
        )

    def test_exception_is_failure(self):

        audit = FinalAudit()

        def broken():

            raise RuntimeError(
                "broken component"
            )

        audit.register(
            "broken",
            broken,
        )

        results = audit.run()

        self.assertFalse(
            results[0].passed
        )

        self.assertIn(
            "broken component",
            results[0].message,
        )


if __name__ == "__main__":
    unittest.main()
