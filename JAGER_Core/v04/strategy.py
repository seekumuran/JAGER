import random


class SearchStrategy:
    def __init__(self, rng):
        self.rng = rng

    def choose(self, exploration_rate):
        value = self.rng.random()

        if value < exploration_rate:
            return "EXPLORE"

        return "EXPLOIT"

    def adjust(self, exploration_rate, discovered):
        if discovered:
            return max(
                0.10,
                exploration_rate - 0.05,
            )

        return min(
            0.80,
            exploration_rate + 0.005,
        )
