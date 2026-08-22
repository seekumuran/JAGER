import unittest

from ..security import SecurityPolicy
from .runner import RedTeamRunner


class TestRedTeamRunner(
    unittest.TestCase
):

    def test_five_scenarios(self):

        runner = RedTeamRunner(
            SecurityPolicy()
        )

        results = runner.run()

        self.assertEqual(
            len(results),
            5,
        )

    def test_all_initial_attacks_blocked(self):

        runner = RedTeamRunner(
            SecurityPolicy()
        )

        results = runner.run()

        self.assertTrue(
            all(
                result["pass"]
                for result in results
            )
        )

    def test_summary(self):

        runner = RedTeamRunner(
            SecurityPolicy()
        )

        results = runner.run()

        summary = runner.summary(
            results
        )

        self.assertEqual(
            summary["total"],
            5,
        )

        self.assertEqual(
            summary["passed"],
            5,
        )

        self.assertEqual(
            summary["failed"],
            0,
        )

        self.assertEqual(
            summary["pass_rate"],
            1.0,
        )


if __name__ == "__main__":
    unittest.main()
