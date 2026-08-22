import random
from typing import Dict, Any, List

from .models import Candidate, Hypothesis


class CandidateGenerator:
    def __init__(self, rng: random.Random):
        self.rng = rng
        self.counter = 0

    def random_candidate(self) -> Dict[str, Any]:
        return {
            "cpu_load": self.rng.uniform(0, 100),
            "memory_load": self.rng.uniform(0, 100),
            "num_processes": self.rng.randint(0, 200),
            "num_threads": self.rng.randint(0, 400),
            "ipc_intensity": self.rng.uniform(0, 100),
        }

    def around(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        def perturb(value, amount, minimum, maximum):
            value = value + self.rng.uniform(-amount, amount)
            return max(minimum, min(maximum, value))

        return {
            "cpu_load": perturb(
                inputs["cpu_load"], 12, 0, 100
            ),
            "memory_load": perturb(
                inputs["memory_load"], 12, 0, 100
            ),
            "num_processes": int(
                perturb(
                    inputs["num_processes"],
                    25,
                    0,
                    200,
                )
            ),
            "num_threads": int(
                perturb(
                    inputs["num_threads"],
                    40,
                    0,
                    400,
                )
            ),
            "ipc_intensity": perturb(
                inputs["ipc_intensity"],
                12,
                0,
                100,
            ),
        }

    def generate(
        self,
        hypotheses: List[Hypothesis],
        experiences,
        count: int = 8,
    ) -> List[Candidate]:

        candidates = []

        useful = experiences.best()

        for _ in range(count):
            self.counter += 1

            if useful is not None and self.rng.random() < 0.65:
                inputs = self.around(useful.inputs)
                strategy = "EXPERIENCE_GUIDED"
                score = 0.7
                hypothesis_id = (
                    hypotheses[0].hypothesis_id
                    if hypotheses
                    else None
                )
            else:
                inputs = self.random_candidate()
                strategy = "EXPLORATION"
                score = 0.5
                hypothesis_id = (
                    hypotheses[-1].hypothesis_id
                    if hypotheses
                    else None
                )

            candidates.append(
                Candidate(
                    candidate_id=f"C-{self.counter:06d}",
                    inputs=inputs,
                    score=score,
                    strategy=strategy,
                    hypothesis_id=hypothesis_id,
                )
            )

        return candidates
