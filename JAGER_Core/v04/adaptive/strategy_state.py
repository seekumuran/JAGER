from dataclasses import dataclass, field
from typing import Dict


@dataclass
class StrategyState:

    iterations: int = 0
    explorations: int = 0
    exploitations: int = 0
    discoveries: int = 0
    target_iterations: Dict[str, int] = field(
        default_factory=dict
    )

    def record_exploration(self):

        self.explorations += 1

    def record_exploitation(self):

        self.exploitations += 1

    def record_discovery(self):

        self.discoveries += 1

    def record_iteration(
        self,
        target: str,
    ):

        self.iterations += 1

        self.target_iterations[
            target
        ] = (
            self.target_iterations.get(
                target,
                0,
            )
            + 1
        )

    def discovery_rate(self):

        total = (
            self.explorations
            + self.exploitations
        )

        if total == 0:
            return 0.0

        return (
            self.discoveries
            / total
        )

    def snapshot(self):

        return {
            "iterations":
                self.iterations,
            "explorations":
                self.explorations,
            "exploitations":
                self.exploitations,
            "discoveries":
                self.discoveries,
            "discovery_rate":
                self.discovery_rate(),
            "target_iterations":
                dict(
                    self.target_iterations
                ),
        }
