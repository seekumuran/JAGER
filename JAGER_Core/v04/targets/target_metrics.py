from dataclasses import dataclass
from typing import Dict, Any, List
import math


@dataclass
class MetricSample:

    target: str
    metric: str
    value: float
    timestamp: float
    experiment_id: str = ""


class TargetMetrics:

    def __init__(self):

        self.samples: List[
            MetricSample
        ] = []

    def record(
        self,
        target: str,
        telemetry: Dict[str, Any],
        timestamp: float,
        experiment_id: str = "",
    ):

        for metric, value in telemetry.items():

            if isinstance(
                value,
                bool,
            ):
                continue

            if isinstance(
                value,
                (int, float),
            ):

                if math.isfinite(
                    float(value)
                ):

                    self.samples.append(
                        MetricSample(
                            target=target,
                            metric=metric,
                            value=float(value),
                            timestamp=timestamp,
                            experiment_id=(
                                experiment_id
                            ),
                        )
                    )

    def values(
        self,
        target: str,
        metric: str,
    ) -> List[float]:

        return [
            sample.value
            for sample in self.samples
            if (
                sample.target == target
                and sample.metric == metric
            )
        ]

    def latest(
        self,
        target: str,
        metric: str,
    ):

        matches = [
            sample
            for sample in self.samples
            if (
                sample.target == target
                and sample.metric == metric
            )
        ]

        if not matches:
            return None

        return matches[-1].value

    def count(
        self,
        target: str,
        metric: str,
    ) -> int:

        return len(
            self.values(
                target,
                metric,
            )
        )

    def summary(
        self,
        target: str,
        metric: str,
    ) -> Dict[str, Any]:

        values = self.values(
            target,
            metric,
        )

        if not values:
            return {
                "count": 0,
                "mean": None,
                "minimum": None,
                "maximum": None,
            }

        return {
            "count": len(values),
            "mean": sum(values)
            / len(values),
            "minimum": min(values),
            "maximum": max(values),
        }

    def target_summary(
        self,
        target: str,
    ):

        metrics = sorted(
            {
                sample.metric
                for sample in self.samples
                if sample.target == target
            }
        )

        return {
            metric: self.summary(
                target,
                metric,
            )
            for metric in metrics
        }
