from dataclasses import dataclass


@dataclass
class ExplorationAllocation:

    exploration: int
    exploitation: int

    @property
    def total(self):

        return (
            self.exploration
            + self.exploitation
        )


class ExplorationScheduler:

    def __init__(
        self,
        minimum_exploration: int = 1,
    ):

        if minimum_exploration < 0:
            raise ValueError(
                "minimum_exploration "
                "cannot be negative"
            )

        self.minimum_exploration = (
            minimum_exploration
        )

    def allocate(
        self,
        budget: int,
        exploration_rate: float,
    ):

        if budget < 0:
            raise ValueError(
                "budget cannot be negative"
            )

        if not 0 <= exploration_rate <= 1:
            raise ValueError(
                "exploration_rate must "
                "be between 0 and 1"
            )

        if budget == 0:
            return ExplorationAllocation(
                0,
                0,
            )

        exploration = int(
            budget
            * exploration_rate
        )

        if (
            exploration_rate > 0
            and exploration < (
                self.minimum_exploration
            )
        ):

            exploration = min(
                self.minimum_exploration,
                budget,
            )

        exploitation = (
            budget
            - exploration
        )

        return ExplorationAllocation(
            exploration=exploration,
            exploitation=exploitation,
        )
