from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class TerminationDecision:

    should_stop: bool

    reason: str

    status: str

    metadata: Dict[str, Any]


class TerminationController:

    TERMINAL_STATUSES = {
        "completed",
        "failed",
        "cancelled",
        "terminated",
    }

    def __init__(
        self,
        target_score: Optional[float] = None,
        maximum_iterations: Optional[int] = None,
    ):

        self.target_score = target_score
        self.maximum_iterations = (
            maximum_iterations
        )

    def evaluate(
        self,
        iteration: int,
        status: str = "running",
        score: Optional[float] = None,
        error: Optional[str] = None,
    ) -> TerminationDecision:

        if status in self.TERMINAL_STATUSES:

            return TerminationDecision(
                should_stop=True,
                reason=(
                    f"terminal status: {status}"
                ),
                status=status,
                metadata={
                    "iteration": iteration,
                },
            )

        if error is not None:

            return TerminationDecision(
                should_stop=True,
                reason="runtime error",
                status="failed",
                metadata={
                    "iteration": iteration,
                    "error": error,
                },
            )

        if (
            self.target_score is not None
            and score is not None
            and score >= self.target_score
        ):

            return TerminationDecision(
                should_stop=True,
                reason="target score reached",
                status="completed",
                metadata={
                    "iteration": iteration,
                    "score": score,
                    "target_score":
                        self.target_score,
                },
            )

        if (
            self.maximum_iterations is not None
            and iteration >=
                self.maximum_iterations
        ):

            return TerminationDecision(
                should_stop=True,
                reason="iteration limit reached",
                status="completed",
                metadata={
                    "iteration": iteration,
                    "maximum_iterations":
                        self.maximum_iterations,
                },
            )

        return TerminationDecision(
            should_stop=False,
            reason="continue",
            status="running",
            metadata={
                "iteration": iteration,
                "score": score,
            },
        )

    def should_stop(
        self,
        iteration: int,
        status: str = "running",
        score: Optional[float] = None,
    ):

        return self.evaluate(
            iteration=iteration,
            status=status,
            score=score,
        ).should_stop
