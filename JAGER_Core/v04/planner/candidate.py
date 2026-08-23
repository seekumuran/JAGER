from dataclasses import dataclass, field
from typing import Any, Dict
import uuid


@dataclass
class ExperimentCandidate:

    candidate_id: str

    target: str
    action_type: str

    parameters: Dict[str, Any] = field(
        default_factory=dict
    )

    hypothesis: str = ""

    expected_value: float = 0.0
    risk: float = 0.0
    novelty: float = 0.0

    rationale: str = ""

    @classmethod
    def create(
        cls,
        target: str,
        action_type: str,
        parameters=None,
        hypothesis: str = "",
        expected_value: float = 0.0,
        risk: float = 0.0,
        novelty: float = 0.0,
        rationale: str = "",
    ):

        return cls(
            candidate_id=str(uuid.uuid4()),
            target=target,
            action_type=action_type,
            parameters=dict(
                parameters or {}
            ),
            hypothesis=hypothesis,
            expected_value=float(
                expected_value
            ),
            risk=float(risk),
            novelty=float(novelty),
            rationale=rationale,
        )

    def score(self):

        return (
            self.expected_value
            + self.novelty
            - self.risk
        )

    def to_dict(self):

        return {
            "candidate_id":
                self.candidate_id,
            "target": self.target,
            "action_type":
                self.action_type,
            "parameters":
                dict(self.parameters),
            "hypothesis":
                self.hypothesis,
            "expected_value":
                self.expected_value,
            "risk":
                self.risk,
            "novelty":
                self.novelty,
            "score": self.score(),
            "rationale":
                self.rationale,
        }
