from dataclasses import dataclass


@dataclass
class JagerConfig:
    seed: int = 42
    budget: int = 1000
    memory_capacity: int = 10000
    exploration_rate: float = 0.45
    reproduction_attempts: int = 3
    stop_on_confirmed_failure: bool = False
