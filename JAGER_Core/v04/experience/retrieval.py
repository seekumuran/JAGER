from dataclasses import dataclass
from typing import List

from .experience_record import (
    ExperienceRecord,
)


@dataclass
class RetrievalResult:

    experience_id: str
    score: float
    reason: str

    def to_dict(self):

        return {
            "experience_id":
                self.experience_id,
            "score":
                self.score,
            "reason":
                self.reason,
        }


class ExperienceRetriever:

    def retrieve(
        self,
        experiences: List[
            ExperienceRecord
        ],
        target: str,
        tags=None,
        limit: int = 5,
    ):

        if limit <= 0:
            return []

        query_tags = set(
            tags or []
        )

        results = []

        for experience in experiences:

            score = 0.0
            reasons = []

            if experience.target == target:

                score += 1.0
                reasons.append(
                    "same_target"
                )

            overlap = (
                query_tags
                & set(experience.tags)
            )

            if overlap:

                score += (
                    0.25
                    * len(overlap)
                )

                reasons.append(
                    "tag_overlap"
                )

            if experience.discovery:

                score += 0.10
                reasons.append(
                    "discovery"
                )

            score += (
                min(
                    max(
                        experience.confidence,
                        0.0,
                    ),
                    1.0,
                )
                * 0.10
            )

            if score > 0:

                results.append(
                    RetrievalResult(
                        experience_id=(
                            experience
                            .experience_id
                        ),
                        score=score,
                        reason=",".join(
                            reasons
                        ),
                    )
                )

        results.sort(
            key=lambda result:
                result.score,
            reverse=True,
        )

        return results[:limit]
