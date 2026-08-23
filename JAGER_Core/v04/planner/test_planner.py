import unittest

from .goal import Goal
from .candidate import (
    ExperimentCandidate,
)
from .candidate_ranker import (
    CandidateRanker,
)
from .planner import (
    ExperimentPlanner,
)


class TestPlanner(
    unittest.TestCase
):

    def test_goal(self):

        goal = Goal.create(
            target="mock",
            objective=(
                "Understand target behavior."
            ),
            constraints={
                "maximum_risk": 0.5
            },
            success_criteria=[
                "behavior observed"
            ],
            priority=0.8,
        )

        self.assertEqual(
            goal.target,
            "mock",
        )

        self.assertEqual(
            goal.priority,
            0.8,
        )

    def test_candidate_score(self):

        candidate = (
            ExperimentCandidate.create(
                target="mock",
                action_type="probe",
                expected_value=0.8,
                novelty=0.6,
                risk=0.2,
            )
        )

        self.assertAlmostEqual(
            candidate.score(),
            1.2,
        )

    def test_ranker(self):

        candidates = [
            ExperimentCandidate.create(
                target="mock",
                action_type="observe",
                expected_value=0.5,
                novelty=0.1,
                risk=0.0,
            ),
            ExperimentCandidate.create(
                target="mock",
                action_type="probe",
                expected_value=0.8,
                novelty=0.6,
                risk=0.2,
            ),
        ]

        ranker = CandidateRanker()

        ranked = ranker.rank(
            candidates
        )

        self.assertEqual(
            ranked[0].action_type,
            "probe",
        )

    def test_risk_filter(self):

        candidate = (
            ExperimentCandidate.create(
                target="mock",
                action_type="probe",
                risk=0.9,
            )
        )

        ranker = CandidateRanker()

        self.assertIsNone(
            ranker.best(
                [candidate],
                maximum_risk=0.5,
            )
        )

    def test_planner(self):

        goal = Goal.create(
            target="mock",
            objective="Study behavior",
            constraints={
                "maximum_risk": 0.5
            },
        )

        planner = ExperimentPlanner()

        result = planner.plan(
            goal
        )

        self.assertGreater(
            len(result["candidates"]),
            0,
        )

        self.assertIsNotNone(
            result["best"]
        )


if __name__ == "__main__":
    unittest.main()
