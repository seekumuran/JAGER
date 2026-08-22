from typing import List

from .models import Hypothesis


class HypothesisEngine:
    def __init__(self):
        self.counter = 0

    def generate(self, experience_memory) -> List[Hypothesis]:
        hypotheses = []

        self.counter += 1

        recent = experience_memory.recent()

        if not recent:
            hypotheses.append(
                Hypothesis(
                    hypothesis_id=f"H-{self.counter:05d}",
                    description="Failure may emerge from interacting system variables.",
                    confidence=0.30,
                    source="initial",
                )
            )
            return hypotheses

        failed = [
            item for item in recent
            if item.status == "FAILED"
        ]

        if failed:
            self.counter += 1

            hypotheses.append(
                Hypothesis(
                    hypothesis_id=f"H-{self.counter:05d}",
                    description=(
                        "The failure region may be near previously observed "
                        "failure conditions."
                    ),
                    confidence=0.75,
                    source="experience",
                )
            )

        self.counter += 1

        hypotheses.append(
            Hypothesis(
                hypothesis_id=f"H-{self.counter:05d}",
                description=(
                    "A previously unexplored combination of system variables "
                    "may expose a hidden failure."
                ),
                confidence=0.50,
                source="exploration",
            )
        )

        return hypotheses
