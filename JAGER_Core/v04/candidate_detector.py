from .candidates import (
    Candidate,
    CandidateStore,
)


class CandidateDetector:

    def __init__(
        self,
        store=None,
    ):
        self.store = (
            store
            or CandidateStore()
        )

        self.counter = 0

    def inspect(
        self,
        experiment,
    ):
        observation = experiment.get(
            "observation"
        )

        if observation is None:
            return None

        status = observation.status

        if status != "FAILED":
            return None

        self.counter += 1

        action = experiment[
            "action"
        ]

        experience = experiment[
            "experience"
        ]

        candidate = Candidate(
            candidate_id=(
                f"candidate-{self.counter:06d}"
            ),
            experiment_id=(
                experiment[
                    "experiment_id"
                ]
            ),
            inputs=dict(
                action.parameters
            ),
            status=status,
            novelty=experience.novelty,
            reward=experience.reward,
        )

        self.store.add(
            candidate
        )

        return candidate
