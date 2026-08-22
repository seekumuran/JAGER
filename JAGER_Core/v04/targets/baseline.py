from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Baseline:

    target: str
    metrics: Dict[str, Dict[str, float]]
    samples: int


class BaselineBuilder:

    def build(
        self,
        metrics,
        target: str,
    ) -> Baseline:

        summary = metrics.target_summary(
            target
        )

        return Baseline(
            target=target,
            metrics=summary,
            samples=self._sample_count(
                metrics,
                target,
            ),
        )

    @staticmethod
    def _sample_count(
        metrics,
        target: str,
    ) -> int:

        samples = [
            sample
            for sample in metrics.samples
            if sample.target == target
        ]

        return len(samples)


class BaselineComparator:

    def compare(
        self,
        baseline: Baseline,
        telemetry: Dict[str, float],
    ) -> Dict[str, Dict[str, float]]:

        result = {}

        for metric, value in telemetry.items():

            if metric not in baseline.metrics:
                continue

            if not isinstance(
                value,
                (int, float),
            ):
                continue

            stats = baseline.metrics[
                metric
            ]

            mean = stats.get(
                "mean"
            )

            if mean is None:
                continue

            delta = float(value) - mean

            result[metric] = {
                "value": float(value),
                "baseline_mean": mean,
                "delta": delta,
            }

        return result
