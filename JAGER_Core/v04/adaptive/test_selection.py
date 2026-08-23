import unittest

from .candidate import Candidate
from .scorer import (
    CandidateScorer,
)
from .selector import (
    CandidateSelector,
)


class TestSelection(
    unittest.TestCase
):

    def setUp(self):

        self.candidates = [
            Candidate(
                f"cand-{i}",
                "blackbox",
                {"x": i},
            )
            for i in range(3)
        ]

        scorer = CandidateScorer()

        self.scores = [
            scorer.score(
                "cand-0",
                0.1,
                0.1,
                0.1,
            ),
            scorer.score(
                "cand-1",
                0.9,
                0.8,
                0.7,
            ),
            scorer.score(
                "cand-2",
                0.4,
                0.3,
                0.2,
            ),
        ]

    def test_best_candidate(self):

        selector = CandidateSelector(
            seed=42,
            exploration_rate=0.0,
        )

        selected = selector.select(
            self.candidates,
            self.scores,
            1,
        )

        self.assertEqual(
            selected[0].candidate_id,
            "cand-1",
        )

    def test_multiple_selection(self):

        selector = CandidateSelector(
            seed=42,
            exploration_rate=0.0,
        )

        selected = selector.select(
            self.candidates,
            self.scores,
            3,
        )

        self.assertEqual(
            len(selected),
            3,
        )

        self.assertEqual(
            len(
                {
                    item.candidate_id
                    for item in selected
                }
            ),
            3,
        )

    def test_empty_selection(self):

        selector = CandidateSelector()

        self.assertEqual(
            selector.select(
                [],
                [],
                1,
            ),
            [],
        )


if __name__ == "__main__":
    unittest.main()
