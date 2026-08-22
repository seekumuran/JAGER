from dataclasses import dataclass
from typing import Dict, Any, Optional
import math


@dataclass
class Anomaly:

    metric: str
    value: float
    baseline_mean: float
    deviation: float
    score: float
    anomalous: bool

    def to_dict(self):
        return {
            "metric": self.metric,
            "value": self.value,
            "baseline_mean": self.baseline_mean,
            "deviation": self.deviation,
            "score": self.score,
            "anomalous": self.anomalous,
        }


class AnomalyDetector:

    def __init__(
        self,
        threshold: float = 2.0,
        minimum_samples: int = 2,
    ):
        self.threshold = float(threshold)
        self.minimum_samples = int(
            minimum_samples
        )

    def detect(
        self,
        baseline,
        telemetry: Dict[str, Any],
    ):

        results = {}

        if baseline.samples < self.minimum_samples:
            return results

        for metric, value in telemetry.items():

            if not isinstance(
                value,
                (int, float),
            ):
                continue

            if isinstance(
                value,
                bool,
            ):
                continue

            stats = baseline.metrics.get(
                metric
            )

            if not stats:
                continue

            mean = stats.get("mean")

            if mean is None:
                continue

            minimum = stats.get(
                "minimum"
            )

            maximum = stats.get(
                "maximum"
            )

            spread = (
                float(maximum)
                - float(minimum)
            )

            if spread <= 0:
                score = (
                    0.0
                    if float(value) == float(mean)
                    else float("inf")
                )
            else:
                score = abs(
                    float(value)
                    - float(mean)
                ) / spread

            anomalous = (
                score >= self.threshold
            )

            results[metric] = Anomaly(
                metric=metric,
                value=float(value),
                baseline_mean=float(mean),
                deviation=(
                    float(value)
                    - float(mean)
                ),
                score=score,
                anomalous=anomalous,
            )

        return results

    def detect_dict(
        self,
        baseline,
        telemetry: Dict[str, Any],
    ):

        results = self.detect(
            baseline,
            telemetry,
        )

        return {
            metric: anomaly.to_dict()
            for metric, anomaly
            in results.items()
        }

    @staticmethod
    def anomaly_count(
        anomalies,
    ) -> int:

        return sum(
            1
            for anomaly in anomalies.values()
            if anomaly.anomalous
        )

    @staticmethod
    def is_anomalous(
        anomalies,
    ) -> bool:

        return any(
            anomaly.anomalous
            for anomaly
            in anomalies.values()
        )
