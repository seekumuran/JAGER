from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class CandidateScore:

    candidate_id: str
    reward: float
    novelty: float
    anomaly: float
    combined: float

    def to_dict(self):

        return {
            "candidate_id":
                self.candidate_id,
            "reward":
                self.reward,
            "novelty":
                self.novelty,
            "anomaly":
                self.anomaly,
            "combined":
                self.combined,
        }


class CandidateScorer:

    def __init__(
        self,
        reward_weight: float = 0.45,
        novelty_weight: float = 0.30,
        anomaly_weight: float = 0.25,
    ):

        total = (
            reward_weight
            + novelty_weight
            + anomaly_weight
        )

        if total <= 0:
            raise ValueError(
                "At least one score weight "
                "must be positive"
            )

        self.reward_weight = (
            reward_weight / total
        )

        self.novelty_weight = (
            novelty_weight / total
        )

        self.anomaly_weight = (
            anomaly_weight / total
        )

    def score(
        self,
        candidate_id: str,
        reward: float,
        novelty: float,
        anomaly: float,
    ) -> CandidateScore:

        combined = (
            self.reward_weight
            * float(reward)
            + self.novelty_weight
            * float(novelty)
            + self.anomaly_weight
            * float(anomaly)
        )

        return CandidateScore(
            candidate_id=candidate_id,
            reward=float(reward),
            novelty=float(novelty),
            anomaly=float(anomaly),
            combined=combined,
        )

    def rank(
        self,
        scores,
    ):

        return sorted(
            scores,
            key=lambda item:
                item.combined,
            reverse=True,
        )
