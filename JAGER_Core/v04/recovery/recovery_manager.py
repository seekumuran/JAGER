from typing import Callable, Optional

from .recovery_policy import (
    RecoveryPolicy,
    RecoveryDecision,
)


class RecoveryManager:

    def __init__(
        self,
        policy: Optional[
            RecoveryPolicy
        ] = None,
    ):

        self.policy = (
            policy
            or RecoveryPolicy()
        )

    def execute(
        self,
        operation: Callable,
    ):

        attempt = 0
        last_error = None

        while True:

            try:

                result = operation(
                    attempt
                )

                return {
                    "success": True,
                    "result": result,
                    "attempts": attempt + 1,
                    "error": None,
                }

            except Exception as exc:

                last_error = exc

                decision = (
                    self.policy.decide(
                        attempt=attempt,
                        error=exc,
                    )
                )

                if not decision.retry:

                    return {
                        "success": False,
                        "result": None,
                        "attempts":
                            attempt + 1,
                        "error":
                            str(last_error),
                        "decision":
                            decision,
                    }

                attempt = (
                    decision.next_attempt
                )
