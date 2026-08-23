from dataclasses import dataclass


@dataclass
class RiskBudget:

    maximum: float = 1.0

    consumed: float = 0.0

    def validate(self):

        if not 0.0 <= self.maximum <= 1.0:

            raise ValueError(
                "maximum risk must be "
                "between 0 and 1"
            )

        if self.consumed < 0.0:

            raise ValueError(
                "consumed risk cannot "
                "be negative"
            )

    def available(self):

        self.validate()

        return max(
            0.0,
            self.maximum
            - self.consumed,
        )

    def can_consume(
        self,
        amount: float,
    ):

        if amount < 0.0:

            raise ValueError(
                "risk amount cannot "
                "be negative"
            )

        return (
            self.consumed + amount
            <= self.maximum
        )

    def consume(
        self,
        amount: float,
    ):

        if not self.can_consume(
            amount
        ):

            raise RuntimeError(
                "Risk budget exhausted"
            )

        self.consumed += amount

    def reset(self):

        self.consumed = 0.0

    def snapshot(self):

        return {
            "maximum":
                self.maximum,
            "consumed":
                self.consumed,
            "available":
                self.available(),
        }
