from typing import List

from .candidate import (
    ExperimentCandidate,
)

from .goal import Goal


class CandidateGenerator:

    def generate(
        self,
        goal: Goal,
        previous_experiences=None,
    ) -> List[
        ExperimentCandidate
    ]:

        candidates = []

        candidates.append(
            ExperimentCandidate.create(
                target=goal.target,
                action_type="observe",
                hypothesis=(
                    "Observation will establish "
                    "the current target state."
                ),
                expected_value=0.5,
                risk=0.0,
                novelty=0.1,
                rationale=(
                    "Establish a baseline before "
                    "active experimentation."
                ),
            )
        )

        candidates.append(
            ExperimentCandidate.create(
                target=goal.target,
                action_type="probe",
                parameters={
                    "intensity": 0.25
                },
                hypothesis=(
                    "A low-intensity probe will "
                    "reveal target behavior."
                ),
                expected_value=0.7,
                risk=0.1,
                novelty=0.4,
                rationale=(
                    "Prefer a low-risk probe "
                    "before stronger actions."
                ),
            )
        )

        if previous_experiences:

            candidates.append(
                ExperimentCandidate.create(
                    target=goal.target,
                    action_type="probe",
                    parameters={
                        "intensity": 0.50
                    },
                    hypothesis=(
                        "A stronger probe may "
                        "expose behavior missed "
                        "by the baseline."
                    ),
                    expected_value=0.8,
                    risk=0.25,
                    novelty=0.6,
                    rationale=(
                        "Generated from prior "
                        "experience availability."
                    ),
                )
            )

        return candidates
