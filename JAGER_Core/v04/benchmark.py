from dataclasses import dataclass, asdict
from typing import Dict, List


@dataclass
class BenchmarkResult:

    total_experiments: int
    total_candidates: int
    verified_discoveries: int

    discovery_rate: float
    verification_rate: float

    normal_observations: int
    degraded_observations: int
    failed_observations: int

    average_novelty: float
    average_reward: float

    def to_dict(self) -> Dict:
        return asdict(self)


class Benchmark:

    def __init__(self, hunter, discovery_pipeline):
        self.hunter = hunter
        self.discovery_pipeline = (
            discovery_pipeline
        )

    def evaluate(self) -> BenchmarkResult:

        experiments = (
            self.hunter.experiments
        )

        total = len(experiments)

        candidates = (
            self.discovery_pipeline.candidates()
        )

        verified = (
            self.discovery_pipeline.discoveries()
        )

        normal = 0
        degraded = 0
        failed = 0

        novelty_values = []
        reward_values = []

        for experiment in experiments:

            observation = experiment.get(
                "observation"
            )

            experience = experiment.get(
                "experience"
            )

            if observation is not None:

                status = observation.status

                if status == "NORMAL":
                    normal += 1

                elif status == "DEGRADED":
                    degraded += 1

                elif status == "FAILED":
                    failed += 1

            if experience is not None:
                novelty_values.append(
                    experience.novelty
                )

                reward_values.append(
                    experience.reward
                )

        discovery_rate = (
            len(verified) / total
            if total
            else 0.0
        )

        verification_rate = (
            len(verified) / len(candidates)
            if candidates
            else 0.0
        )

        average_novelty = (
            sum(novelty_values)
            / len(novelty_values)
            if novelty_values
            else 0.0
        )

        average_reward = (
            sum(reward_values)
            / len(reward_values)
            if reward_values
            else 0.0
        )

        return BenchmarkResult(
            total_experiments=total,
            total_candidates=len(candidates),
            verified_discoveries=len(verified),
            discovery_rate=discovery_rate,
            verification_rate=verification_rate,
            normal_observations=normal,
            degraded_observations=degraded,
            failed_observations=failed,
            average_novelty=average_novelty,
            average_reward=average_reward,
        )
