from dataclasses import dataclass, field
from typing import Dict


@dataclass
class ResourceBudget:

    max_iterations: int = 10

    max_failures: int = 3

    max_actions: int = 100

    max_risk: float = 1.0

    consumed_iterations: int = 0

    consumed_failures: int = 0

    consumed_actions: int = 0

    metadata: Dict = field(
        default_factory=dict
    )

    def can_iterate(self):

        return (
            self.consumed_iterations
            < self.max_iterations
        )

    def can_fail(self):

        return (
            self.consumed_failures
            < self.max_failures
        )

    def can_act(
        self,
        count: int = 1,
    ):

        return (
            self.consumed_actions
            + count
            <= self.max_actions
        )

    def consume_iteration(self):

        if not self.can_iterate():

            raise RuntimeError(
                "Iteration budget exhausted"
            )

        self.consumed_iterations += 1

    def consume_failure(self):

        if not self.can_fail():

            raise RuntimeError(
                "Failure budget exhausted"
            )

        self.consumed_failures += 1

    def consume_actions(
        self,
        count: int = 1,
    ):

        if count < 0:

            raise ValueError(
                "count cannot be negative"
            )

        if not self.can_act(count):

            raise RuntimeError(
                "Action budget exhausted"
            )

        self.consumed_actions += count

    def remaining_iterations(self):

        return (
            self.max_iterations
            - self.consumed_iterations
        )

    def remaining_failures(self):

        return (
            self.max_failures
            - self.consumed_failures
        )

    def remaining_actions(self):

        return (
            self.max_actions
            - self.consumed_actions
        )

    def snapshot(self):

        return {
            "max_iterations":
                self.max_iterations,
            "max_failures":
                self.max_failures,
            "max_actions":
                self.max_actions,
            "max_risk":
                self.max_risk,
            "consumed_iterations":
                self.consumed_iterations,
            "consumed_failures":
                self.consumed_failures,
            "consumed_actions":
                self.consumed_actions,
            "remaining_iterations":
                self.remaining_iterations(),
            "remaining_failures":
                self.remaining_failures(),
            "remaining_actions":
                self.remaining_actions(),
            "metadata":
                dict(self.metadata),
        }
