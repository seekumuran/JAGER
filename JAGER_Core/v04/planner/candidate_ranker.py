from typing import List

from .candidate import (
    ExperimentCandidate,
)


class CandidateRanker:

    def rank(
        self,
        candidates: List[
            ExperimentCandidate
        ],
        maximum_risk: float = 1.0,
    ):

        eligible = [
            candidate
            for candidate in candidates
            if candidate.risk
            <= maximum_risk
        ]

        return sorted(
            eligible,
            key=lambda candidate:
                candidate.score(),
            reverse=True,
        )

    def best(
        self,
        candidates,
        maximum_risk: float = 1.0,
    ):

        ranked = self.rank(
            candidates,
            maximum_risk,
        )

        if not ranked:
            return None

        return ranked[0]
