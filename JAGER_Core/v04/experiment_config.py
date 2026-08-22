from dataclasses import dataclass, asdict


@dataclass
class ExperimentConfig:
    seed: int = 42
    budget: int = 100
    exploration_rate: float = 0.30
    memory_capacity: int = 1000
    target_name: str = "blackbox"
    version: str = "0.4.0"

    def __post_init__(self):
        if self.budget <= 0:
            raise ValueError(
                "budget must be greater than zero"
            )

        if not 0.0 <= self.exploration_rate <= 1.0:
            raise ValueError(
                "exploration_rate must be between 0 and 1"
            )

        if self.memory_capacity <= 0:
            raise ValueError(
                "memory_capacity must be greater than zero"
            )

        if not self.target_name:
            raise ValueError(
                "target_name cannot be empty"
            )

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(
            seed=int(data.get("seed", 42)),
            budget=int(data.get("budget", 100)),
            exploration_rate=float(
                data.get(
                    "exploration_rate",
                    0.30,
                )
            ),
            memory_capacity=int(
                data.get(
                    "memory_capacity",
                    1000,
                )
            ),
            target_name=data.get(
                "target_name",
                "blackbox",
            ),
            version=data.get(
                "version",
                "0.4.0",
            ),
        )
