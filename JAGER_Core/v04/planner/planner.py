from typing import Optional

from .candidate_generator import (
    CandidateGenerator,
)

from .candidate_ranker import (
    CandidateRanker,
)

from .goal import Goal


class ExperimentPlanner:

    def __init__(
        self,
        generator: Optional[
            CandidateGenerator
        ] = None,
        ranker: Optional[
            CandidateRanker
        ] = None,
    ):

        self.generator = (
            generator
            or CandidateGenerator()
        )

        self.ranker = (
            ranker
            or CandidateRanker()
        )

    def plan(
        self,
        goal: Goal,
        previous_experiences=None,
    ):

        candidates = (
            self.generator.generate(
                goal,
                previous_experiences,
            )
        )

        maximum_risk = float(
            goal.constraints.get(
                "maximum_risk",
                1.0,
            )
        )

        ranked = self.ranker.rank(
            candidates,
            maximum_risk,
        )

        return {
            "goal": goal,
            "candidates": candidates,
            "ranked": ranked,
            "best": (
                ranked[0]
                if ranked
                else None
            ),
        }
