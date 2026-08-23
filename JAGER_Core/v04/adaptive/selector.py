import random
from typing import List

from .candidate import Candidate
from .scorer import CandidateScore


class CandidateSelector:

    def __init__(
        self,
        seed: int = 42,
        exploration_rate: float = 0.20,
    ):

        if not 0 <= exploration_rate <= 1:
            raise ValueError(
                "exploration_rate must "
                "be between 0 and 1"
            )

        self.rng = random.Random(seed)
        self.exploration_rate = (
            exploration_rate
        )

    def select(
        self,
        candidates: List[Candidate],
        scores: List[CandidateScore],
        count: int = 1,
    ):

        if count <= 0:
            return []

        if not candidates:
            return []

        score_map = {
            score.candidate_id:
                score
            for score in scores
        }

        ranked = sorted(
            candidates,
            key=lambda candidate:
                score_map.get(
                    candidate.candidate_id
                ).combined
                if candidate.candidate_id
                in score_map
                else float("-inf"),
            reverse=True,
        )

        selected = []

        for _ in range(
            min(count, len(ranked))
        ):

            if (
                self.rng.random()
                < self.exploration_rate
            ):

                available = [
                    candidate
                    for candidate
                    in ranked
                    if candidate
                    not in selected
                ]

                if not available:
                    break

                choice = self.rng.choice(
                    available
                )

            else:

                choice = next(
                    (
                        candidate
                        for candidate
                        in ranked
                        if candidate
                        not in selected
                    ),
                    None,
                )

                if choice is None:
                    break

            selected.append(choice)

        return selected
