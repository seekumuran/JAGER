from typing import Dict, Any


class ReproductionEngine:
    def __init__(self, system):
        self.system = system

    def reproduce(
        self,
        inputs: Dict[str, Any],
        attempts: int = 3,
    ) -> int:

        successes = 0

        for _ in range(attempts):
            result = self.system.observe(**inputs)

            if result["status"] == "FAILED":
                successes += 1

        return successes
