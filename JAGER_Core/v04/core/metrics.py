from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import statistics


@dataclass
class MetricSample:

    name: str

    value: float

    iteration: Optional[int] = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self):

        return {
            "name": self.name,
            "value": self.value,
            "iteration": self.iteration,
            "metadata": dict(self.metadata),
        }


class MetricSeries:

    def __init__(
        self,
        name: str,
    ):

        self.name = name

        self._samples: List[
            MetricSample
        ] = []

    def add(
        self,
        value: float,
        iteration: Optional[int] = None,
        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ):

        sample = MetricSample(
            name=self.name,
            value=float(value),
            iteration=iteration,
            metadata=dict(
                metadata or {}
            ),
        )

        self._samples.append(
            sample
        )

        return sample

    def values(self):

        return [
            sample.value
            for sample
            in self._samples
        ]

    def latest(self):

        if not self._samples:

            return None

        return self._samples[-1]

    def count(self):

        return len(
            self._samples
        )

    def mean(self):

        values = self.values()

        if not values:

            return None

        return statistics.mean(values)

    def minimum(self):

        values = self.values()

        if not values:

            return None

        return min(values)

    def maximum(self):

        values = self.values()

        if not values:

            return None

        return max(values)

    def snapshot(self):

        return {
            "name": self.name,
            "count": self.count(),
            "mean": self.mean(),
            "minimum": self.minimum(),
            "maximum": self.maximum(),
            "latest": (
                self.latest().to_dict()
                if self.latest()
                else None
            ),
            "samples": [
                sample.to_dict()
                for sample
                in self._samples
            ],
        }


class MetricsRegistry:

    def __init__(self):

        self._series: Dict[
            str,
            MetricSeries,
        ] = {}

    def series(
        self,
        name: str,
    ):

        if name not in self._series:

            self._series[name] = (
                MetricSeries(name)
            )

        return self._series[name]

    def record(
        self,
        name: str,
        value: float,
        iteration: Optional[int] = None,
        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ):

        return self.series(
            name
        ).add(
            value,
            iteration,
            metadata,
        )

    def get(
        self,
        name: str,
    ):

        return self._series.get(
            name
        )

    def names(self):

        return list(
            self._series.keys()
        )

    def snapshot(self):

        return {
            name: series.snapshot()
            for name, series
            in self._series.items()
        }

    def clear(self):

        self._series.clear()
