from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass
class Candidate:

    candidate_id: str
    experiment_id: str
    inputs: Dict[str, Any]
    status: str
    novelty: float
    reward: float

    verification_attempts: int = 0
    verified: bool = False

    def record_verification(
        self,
        confirmed: bool,
    ):
        self.verification_attempts += 1

        if confirmed:
            self.verified = True

    def to_dict(self):
        return asdict(self)


class CandidateStore:

    def __init__(self):
        self.candidates: List[
            Candidate
        ] = []

    def add(
        self,
        candidate: Candidate,
    ):
        self.candidates.append(
            candidate
        )

    def all(self):
        return list(self.candidates)

    def verified(self):
        return [
            candidate
            for candidate in self.candidates
            if candidate.verified
        ]

    def unverified(self):
        return [
            candidate
            for candidate in self.candidates
            if not candidate.verified
        ]

    def count(self):
        return len(self.candidates)

    def verification_rate(self):

        if not self.candidates:
            return 0.0

        return (
            len(self.verified())
            / len(self.candidates)
        )
