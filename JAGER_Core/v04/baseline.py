import random


class RandomBaseline:
    """
    Random-search baseline.

    This intentionally has no learning,
    memory, hypothesis generation, or
    experience-guided search.
    """

    def __init__(self, target, seed=42):
        self.target = target
        self.rng = random.Random(seed)

    def generate(self):
        return {
            "cpu_load": self.rng.uniform(0, 100),
            "memory_load": self.rng.uniform(0, 100),
            "num_processes": self.rng.randint(
                0,
                200,
            ),
            "num_threads": self.rng.randint(
                0,
                400,
            ),
            "ipc_intensity": self.rng.uniform(
                0,
                100,
            ),
        }

    def run(self, budget):
        results = []

        for _ in range(budget):
            inputs = self.generate()

            result = self.target.observe(
                **inputs
            )

            results.append(
                {
                    "inputs": inputs,
                    "result": result,
                }
            )

        return results
