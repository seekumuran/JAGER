from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class ClassificationResult:

    is_discovery: bool
    category: str
    severity: str

    novelty: float
    confidence: float

    reason: str

    def to_dict(self):

        return {
            "is_discovery":
                self.is_discovery,
            "category":
                self.category,
            "severity":
                self.severity,
            "novelty":
                self.novelty,
            "confidence":
                self.confidence,
            "reason":
                self.reason,
        }


class DiscoveryClassifier:

    def __init__(
        self,
        novelty_threshold: float = 0.60,
        confidence_threshold: float = 0.70,
    ):

        self.novelty_threshold = (
            novelty_threshold
        )

        self.confidence_threshold = (
            confidence_threshold
        )

    def classify(
        self,
        observation: Dict[str, Any],
        baseline: Optional[
            Dict[str, Any]
        ] = None,
    ) -> ClassificationResult:

        novelty = self._novelty(
            observation,
            baseline or {},
        )

        confidence = self._confidence(
            observation
        )

        category = self._category(
            observation
        )

        severity = self._severity(
            observation
        )

        is_discovery = (
            novelty
            >= self.novelty_threshold
            and confidence
            >= self.confidence_threshold
        )

        if is_discovery:

            reason = (
                "Observation exceeds the "
                "configured novelty and "
                "confidence thresholds."
            )

        else:

            reason = (
                "Observation does not meet "
                "the discovery thresholds."
            )

        return ClassificationResult(
            is_discovery=is_discovery,
            category=category,
            severity=severity,
            novelty=novelty,
            confidence=confidence,
            reason=reason,
        )

    def _novelty(
        self,
        observation,
        baseline,
    ):

        if not baseline:
            return 1.0

        differences = 0
        comparable = 0

        for key, value in observation.items():

            if key not in baseline:
                differences += 1
                comparable += 1
                continue

            comparable += 1

            if baseline[key] != value:
                differences += 1

        if comparable == 0:
            return 0.0

        return min(
            1.0,
            differences / comparable,
        )

    def _confidence(
        self,
        observation,
    ):

        explicit = observation.get(
            "confidence"
        )

        if explicit is not None:

            return max(
                0.0,
                min(
                    1.0,
                    float(explicit),
                ),
            )

        if observation.get(
            "status"
        ) == "failure":

            return 0.90

        if observation.get(
            "anomaly"
        ):

            return 0.80

        return 0.50

    def _category(
        self,
        observation,
    ):

        if observation.get(
            "security_violation"
        ):

            return "security"

        if observation.get(
            "anomaly"
        ):

            return "anomaly"

        if observation.get(
            "status"
        ) == "failure":

            return "failure"

        return "behavioral"

    def _severity(
        self,
        observation,
    ):

        severity = observation.get(
            "severity"
        )

        if severity in {
            "low",
            "medium",
            "high",
            "critical",
        }:

            return severity

        if observation.get(
            "security_violation"
        ):

            return "high"

        return "low"
