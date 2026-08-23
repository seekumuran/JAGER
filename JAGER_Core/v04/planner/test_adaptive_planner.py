import unittest

from .adaptive_planner import (
    AdaptivePlanner,
)

from .goal import Goal


class TestAdaptivePlanner(
    unittest.TestCase
):

    def test_initial_plan(self):

        planner = AdaptivePlanner()

        goal = Goal.create(
            target="mock",
            objective=(
                "Discover target behavior."
            ),
            constraints={
                "maximum_risk": 0.5
            },
        )

        plan = planner.initial_plan(
            goal
        )

        self.assertIsNotNone(
            plan["best"]
        )

        self.assertGreater(
            len(plan["candidates"]),
            0,
        )

    def test_update_plan(self):

        planner = AdaptivePlanner()

        goal = Goal.create(
            target="mock",
            objective="Explore",
        )

        initial = planner.initial_plan(
            goal
        )

        updated = planner.update(
            goal=goal,
            plan=initial,
            observations=[
                {
                    "action_type":
                        "observe"
                }
            ],
            discoveries=[],
            experiences=[],
        )

        self.assertGreater(
            len(updated["ranked"]),
            0,
        )

        self.assertIsNotNone(
            updated["best"]
        )


if __name__ == "__main__":
    unittest.main()
