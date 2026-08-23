import unittest

from .resource_budget import (
    ResourceBudget,
)

from .risk_budget import (
    RiskBudget,
)

from .budget_manager import (
    BudgetManager,
)


class TestResourceBudget(
    unittest.TestCase
):

    def test_iterations(self):

        budget = ResourceBudget(
            max_iterations=2
        )

        self.assertTrue(
            budget.can_iterate()
        )

        budget.consume_iteration()
        budget.consume_iteration()

        self.assertFalse(
            budget.can_iterate()
        )

        self.assertEqual(
            budget.remaining_iterations(),
            0,
        )

    def test_actions(self):

        budget = ResourceBudget(
            max_actions=5
        )

        budget.consume_actions(3)

        self.assertEqual(
            budget.remaining_actions(),
            2,
        )

        with self.assertRaises(
            RuntimeError
        ):

            budget.consume_actions(3)


class TestRiskBudget(
    unittest.TestCase
):

    def test_risk(self):

        budget = RiskBudget(
            maximum=0.5
        )

        self.assertTrue(
            budget.can_consume(0.3)
        )

        budget.consume(0.3)

        self.assertAlmostEqual(
            budget.available(),
            0.2,
        )

    def test_exhausted(self):

        budget = RiskBudget(
            maximum=0.5
        )

        budget.consume(0.5)

        with self.assertRaises(
            RuntimeError
        ):

            budget.consume(0.1)


class TestBudgetManager(
    unittest.TestCase
):

    def test_manager(self):

        manager = BudgetManager(
            resources=ResourceBudget(
                max_iterations=3,
                max_actions=10,
            ),
            risk=RiskBudget(
                maximum=1.0
            ),
        )

        manager.begin_iteration()
        manager.record_actions(2)
        manager.record_risk(0.2)

        snapshot = (
            manager.snapshot()
        )

        self.assertEqual(
            snapshot[
                "resources"
            ][
                "consumed_iterations"
            ],
            1,
        )

        self.assertEqual(
            snapshot[
                "resources"
            ][
                "consumed_actions"
            ],
            2,
        )

        self.assertAlmostEqual(
            snapshot[
                "risk"
            ][
                "consumed"
            ],
            0.2,
        )

        self.assertTrue(
            snapshot["can_continue"]
        )


if __name__ == "__main__":
    unittest.main()
