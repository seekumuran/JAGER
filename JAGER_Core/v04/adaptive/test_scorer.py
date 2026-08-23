import unittest

from .scorer import (
    CandidateScorer,
)


class TestCandidateScorer(
    unittest.TestCase
):

    def test_weighted_score(self):

        scorer = CandidateScorer(
            reward_weight=1.0,
            novelty_weight=0.0,
            anomaly_weight=0.0,
        )

        result = scorer.score(
            "candidate",
            reward=0.8,
            novelty=0.2,
            anomaly=0.1,
        )

        self.assertAlmostEqual(
            result.combined,
            0.8,
        )

    def test_weights_are_normalized(self):

        scorer = CandidateScorer(
            reward_weight=2.0,
            novelty_weight=1.0,
            anomaly_weight=1.0,
        )

        result = scorer.score(
            "candidate",
            1.0,
            0.0,
            0.0,
        )

        self.assertAlmostEqual(
            result.combined,
            0.5,
        )

    def test_ranking(self):

        scorer = CandidateScorer()

        scores = [
            scorer.score(
                "low",
                0.1,
                0.1,
                0.1,
            ),
            scorer.score(
                "high",
                1.0,
                1.0,
                1.0,
            ),
        ]

        ranked = scorer.rank(
            scores
        )

        self.assertEqual(
            ranked[0].candidate_id,
            "high",
        )


if __name__ == "__main__":
    unittest.main()
