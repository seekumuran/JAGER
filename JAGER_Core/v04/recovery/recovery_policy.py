from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class RecoveryDecision:

    retry: bool
    reason: str
    next_attempt: int


class RecoveryPolicy:

    def __init__(
        self,
        max_retries: int = 2,
    ):

        if max_retries < 0:
            raise ValueError(
                "max_retries cannot be negative"
            )

        self.max_retries = max_retries

    def decide(
        self,
        attempt: int,
        error: Optional[Exception] = None,
    ) -> RecoveryDecision:

        if attempt < 0:
            raise ValueError(
                "attempt cannot be negative"
            )

        if attempt >= self.max_retries:

            return RecoveryDecision(
                retry=False,
                reason=(
                    "maximum retry count reached"
                ),
                next_attempt=attempt,
            )

        reason = (
            str(error)
            if error is not None
            else "recoverable execution failure"
        )

        return RecoveryDecision(
            retry=True,
            reason=reason,
            next_attempt=attempt + 1,
        )
