from typing import Dict, List, Any

from .hunter import JagerHunter
from .hunter_factory import HunterCandidateFactory


class MultiTargetRunner:

    def __init__(
        self,
        runtime,
        targets,
        steps_per_target=10,
        candidate_count=8,
    ):
        self.runtime = runtime
        self.targets = list(targets)
        self.steps_per_target = steps_per_target
        self.candidate_count = candidate_count

        self.results: Dict[str, List[Dict[str, Any]]] = {}

    def run(self):

        for target_name in self.targets:

            self.runtime.select_target(
                target_name
            )

            factory = HunterCandidateFactory(
                target_name=target_name,
                seed=self.runtime.config.seed,
                candidate_count=self.candidate_count,
            )

            hunter = JagerHunter(
                runtime=self.runtime,
                candidate_factory=factory,
            )

            target_results = list(
                hunter.run(
                    self.steps_per_target
                )
            )

            self.results[
                target_name
            ] = target_results

        return self.results

    def summary(self):

        summary = {}

        for target_name, results in (
            self.results.items()
        ):

            total = len(results)

            rewards = [
                float(
                    result.get(
                        "reward",
                        0.0,
                    )
                )
                for result in results
            ]

            denied = sum(
                1
                for result in results
                if result.get(
                    "observation",
                    {},
                ).get(
                    "status"
                ) == "DENIED"
            )

            failed = sum(
                1
                for result in results
                if result.get(
                    "observation",
                    {},
                ).get(
                    "status"
                ) == "FAILED"
            )

            summary[target_name] = {
                "experiments": total,
                "denied": denied,
                "failed": failed,
                "average_reward": (
                    sum(rewards) / total
                    if total
                    else 0.0
                ),
            }

        return summary
