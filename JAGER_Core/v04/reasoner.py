import random

from .models import Action


class HunterReasoner:
    def __init__(self, rng: random.Random):
        self.rng = rng
        self.counter = 0

    def propose(
        self,
        memory,
        exploration_rate: float = 0.35,
    ) -> Action:

        self.counter += 1

        previous = memory.retrieve(limit=1)

        if previous and self.rng.random() > exploration_rate:
            base = previous[0].action.parameters

            def perturb(value, amount, low, high):
                return max(
                    low,
                    min(
                        high,
                        value + self.rng.uniform(-amount, amount),
                    ),
                )

            parameters = {
                "cpu_load": perturb(
                    base["cpu_load"], 10, 0, 100
                ),
                "memory_load": perturb(
                    base["memory_load"], 10, 0, 100
                ),
                "num_processes": int(
                    perturb(
                        base["num_processes"],
                        20,
                        0,
                        200,
                    )
                ),
                "num_threads": int(
                    perturb(
                        base["num_threads"],
                        30,
                        0,
                        400,
                    )
                ),
                "ipc_intensity": perturb(
                    base["ipc_intensity"],
                    10,
                    0,
                    100,
                ),
            }

            operation = "probe"

        else:
            parameters = {
                "cpu_load": self.rng.uniform(0, 100),
                "memory_load": self.rng.uniform(0, 100),
                "num_processes": self.rng.randint(0, 200),
                "num_threads": self.rng.randint(0, 400),
                "ipc_intensity": self.rng.uniform(0, 100),
            }

            operation = "probe"

        return Action(
            action_id=f"action-{self.counter:06d}",
            operation=operation,
            parameters=parameters,
        )
