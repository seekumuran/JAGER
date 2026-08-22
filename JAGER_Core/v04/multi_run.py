from dataclasses import dataclass, asdict
from typing import List, Dict, Any


@dataclass
class RunMetrics:

    run_id: str
    seed: int

    experiments: int
    candidates: int
    verified: int

    normal: int
    degraded: int
    failed: int

    discovery_rate: float
    verification_rate: float

    average_reward: float
    average_novelty: float

    def to_dict(self):
        return asdict(self)


class MultiRunExperiment:

    def __init__(
        self,
        runtime_factory,
        target_name,
        seeds,
    ):
        self.runtime_factory = (
            runtime_factory
        )

        self.target_name = target_name
        self.seeds = list(seeds)

        self.results: List[
            RunMetrics
        ] = []

    def run(self):

        for seed in self.seeds:

            runtime = (
                self.runtime_factory(seed)
            )

            result = runtime.run_protocol(
                self.target_name,
                save=True,
            )

            summary = (
                runtime.executor
                .run.summary
            )

            metrics = RunMetrics(
                run_id=summary.run_id,
                seed=seed,
                experiments=summary.experiments,
                candidates=summary.candidates,
                verified=summary.verified,
                normal=summary.normal,
                degraded=summary.degraded,
                failed=summary.failed,
                discovery_rate=(
                    summary.verified
                    / summary.experiments
                    if summary.experiments
                    else 0.0
                ),
                verification_rate=(
                    summary.verified
                    / summary.candidates
                    if summary.candidates
                    else 0.0
                ),
                average_reward=(
                    self._average(
                        runtime.executor.run.records,
                        "reward",
                    )
                ),
                average_novelty=(
                    self._average(
                        runtime.executor.run.records,
                        "novelty",
                    )
                ),
            )

            self.results.append(
                metrics
            )

        return self.results

    @staticmethod
    def _average(
        records,
        field,
    ):

        if not records:
            return 0.0

        values = [
            getattr(record, field)
            for record in records
        ]

        return sum(values) / len(values)

    def summary(self) -> Dict[str, Any]:

        if not self.results:
            return {
                "runs": 0
            }

        return {
            "runs": len(self.results),

            "total_experiments":
                sum(
                    r.experiments
                    for r in self.results
                ),

            "total_candidates":
                sum(
                    r.candidates
                    for r in self.results
                ),

            "total_verified":
                sum(
                    r.verified
                    for r in self.results
                ),

            "average_discovery_rate":
                self._mean(
                    r.discovery_rate
                    for r in self.results
                ),

            "average_verification_rate":
                self._mean(
                    r.verification_rate
                    for r in self.results
                ),

            "average_reward":
                self._mean(
                    r.average_reward
                    for r in self.results
                ),

            "average_novelty":
                self._mean(
                    r.average_novelty
                    for r in self.results
                ),
        }

    @staticmethod
    def _mean(values):

        values = list(values)

        if not values:
            return 0.0

        return sum(values) / len(values)

    def to_dict(self):

        return {
            "results": [
                result.to_dict()
                for result in self.results
            ],
            "summary": self.summary(),
        }
