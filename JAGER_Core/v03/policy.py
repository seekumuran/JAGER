from dataclasses import dataclass


@dataclass
class AdaptivePolicy:
    exploration_rate: float = 0.35
    exploitation_rate: float = 0.65
    minimum_exploration: float = 0.10
    maximum_exploration: float = 0.90

    def choose_mode(self, random_value: float) -> str:
        if random_value < self.exploration_rate:
            return "EXPLORE"

        return "EXPLOIT"

    def update(self, discovered: bool) -> None:
        if discovered:
            self.exploration_rate = max(
                self.minimum_exploration,
                self.exploration_rate * 0.95,
            )
        else:
            self.exploration_rate = min(
                self.maximum_exploration,
                self.exploration_rate + 0.02,
            )

        self.exploitation_rate = 1.0 - self.exploration_rate
