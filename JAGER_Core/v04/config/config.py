from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class JagerConfig:

    # Runtime
    max_iterations: int = 3
    default_risk_level: str = "low"

    # Planning
    maximum_risk: float = 0.5
    minimum_candidate_score: float = 0.0

    # Discovery
    novelty_threshold: float = 0.60
    confidence_threshold: float = 0.70

    # Experience
    experience_limit: int = 10000

    # Execution
    execution_timeout_ms: float = 30_000.0

    # Safety
    allow_unknown_risk: bool = False

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    def validate(self):

        if self.max_iterations <= 0:
            raise ValueError(
                "max_iterations must be positive"
            )

        if not 0.0 <= self.maximum_risk <= 1.0:
            raise ValueError(
                "maximum_risk must be between 0 and 1"
            )

        if not 0.0 <= self.novelty_threshold <= 1.0:
            raise ValueError(
                "novelty_threshold must be between 0 and 1"
            )

        if not 0.0 <= self.confidence_threshold <= 1.0:
            raise ValueError(
                "confidence_threshold must be between 0 and 1"
            )

        if self.experience_limit <= 0:
            raise ValueError(
                "experience_limit must be positive"
            )

        if self.execution_timeout_ms <= 0:
            raise ValueError(
                "execution_timeout_ms must be positive"
            )

        if self.default_risk_level not in {
            "low",
            "medium",
            "high",
            "unknown",
        }:
            raise ValueError(
                "invalid default_risk_level"
            )

        return self

    def to_dict(self):

        return {
            "max_iterations":
                self.max_iterations,
            "default_risk_level":
                self.default_risk_level,
            "maximum_risk":
                self.maximum_risk,
            "minimum_candidate_score":
                self.minimum_candidate_score,
            "novelty_threshold":
                self.novelty_threshold,
            "confidence_threshold":
                self.confidence_threshold,
            "experience_limit":
                self.experience_limit,
            "execution_timeout_ms":
                self.execution_timeout_ms,
            "allow_unknown_risk":
                self.allow_unknown_risk,
            "metadata":
                dict(self.metadata),
        }
