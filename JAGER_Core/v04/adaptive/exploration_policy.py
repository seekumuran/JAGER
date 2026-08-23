from dataclasses import dataclass
from typing import Dict
import math
import random


@dataclass
class ExplorationState:

    step: int = 0
    total_candidates: int = 0
    selected_candidates: int = 0
    discoveries: int = 0

    def discovery_rate(self):

        if self.selected_candidates == 0:
            return 0.0

        return (
            self.discoveries
            / self.selected_candidates
        )


class ExplorationPolicy:

    def __init__(
        self,
        initial_rate: float = 0.30,
        minimum_rate: float = 0.05,
        maximum_rate: float = 0.80,
        decay: float = 0.01,
        seed: int = 42,
    ):

        if not (
            0.0
            <= minimum_rate
            <= initial_rate
            <= maximum_rate
            <= 1.0
        ):
            raise ValueError(
                "Invalid exploration bounds"
            )

        self.initial_rate = initial_rate
        self.minimum_rate = minimum_rate
        self.maximum_rate = maximum_rate
        self.decay = decay

        self.rng = random.Random(seed)

        self.state = ExplorationState()

    @property
    def rate(self):

        rate = (
            self.initial_rate
            * math.exp(
                -self.decay
                * self.state.step
            )
        )

        return max(
            self.minimum_rate,
            min(
                self.maximum_rate,
                rate,
            ),
        )

    def observe_candidates(
        self,
        count: int,
    ):

        if count < 0:
            raise ValueError(
                "count cannot be negative"
            )

        self.state.total_candidates += count

    def observe_selection(
        self,
        count: int,
    ):

        if count < 0:
            raise ValueError(
                "count cannot be negative"
            )

        self.state.selected_candidates += (
            count
        )

    def observe_discovery(
        self,
        discovered: bool,
    ):

        if discovered:
            self.state.discoveries += 1

    def next_step(self):

        self.state.step += 1

    def should_explore(self):

        return (
            self.rng.random()
            < self.rate
        )

    def snapshot(self):

        return {
            "step": self.state.step,
            "rate": self.rate,
            "total_candidates":
                self.state.total_candidates,
            "selected_candidates":
                self.state.selected_candidates,
            "discoveries":
                self.state.discoveries,
            "discovery_rate":
                self.state.discovery_rate(),
        }
