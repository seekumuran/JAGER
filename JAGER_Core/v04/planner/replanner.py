from typing import Any, Dict, List, Optional

from .candidate import ExperimentCandidate
from .candidate_ranker import CandidateRanker
from .goal import Goal


class Replanner:

    def __init__(
        self,
        ranker: Optional[CandidateRanker] = None,
    ):

        self.ranker = (
            ranker or CandidateRanker()
        )

    def replan(
        self,
        goal: Goal,
        candidates: List[
            ExperimentCandidate
        ],
        observations: Optional[
            List[Dict[str, Any]]
        ] = None,
        discoveries: Optional[
            List[Any]
        ] = None,
        experiences: Optional[
            List[Any]
        ] = None,
    ):

        observations = observations or []
        discoveries = discoveries or []
        experiences = experiences or []

        adjusted = []

        for candidate in candidates:

            expected_value = (
                candidate.expected_value
            )

            risk = candidate.risk
            novelty = candidate.novelty

            # Previous observations should
            # reduce the value of repeating
            # an already-understood action.
            if observations:

                if any(
                    self._same_action(
                        candidate,
                        observation,
                    )
                    for observation
                    in observations
                ):

                    novelty *= 0.5
                    expected_value *= 0.85

            # A validated discovery increases
            # the value of exploring nearby
            # behavior.
            if discoveries:

                novelty = min(
                    1.0,
                    novelty + 0.10,
                )

                expected_value = min(
                    1.0,
                    expected_value + 0.05,
                )

            # Experience should make the
            # planner more selective.
            if experiences:

                risk = max(
                    0.0,
                    risk - 0.05,
                )

            adjusted.append(
                ExperimentCandidate.create(
                    target=candidate.target,
                    action_type=
                        candidate.action_type,
                    parameters=
                        candidate.parameters,
                    hypothesis=
                        candidate.hypothesis,
                    expected_value=
                        expected_value,
                    risk=risk,
                    novelty=novelty,
                    rationale=(
                        candidate.rationale
                        + " Replanned using "
                        "observed execution state."
                    ),
                )
            )

        maximum_risk = float(
            goal.constraints.get(
                "maximum_risk",
                1.0,
            )
        )

        ranked = self.ranker.rank(
            adjusted,
            maximum_risk,
        )

        return {
            "candidates": adjusted,
            "ranked": ranked,
            "best": (
                ranked[0]
                if ranked
                else None
            ),
        }

    @staticmethod
    def _same_action(
        candidate,
        observation,
    ):

        return (
            observation.get("action_type")
            == candidate.action_type
        )
