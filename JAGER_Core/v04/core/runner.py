from typing import Any, Callable, Optional

from .facade import Jager


class JagerRunner:

    def __init__(
        self,
        jager: Jager,
    ):

        self.jager = jager

    def run(
        self,
        experiment_id: str,
        action: Any,
        *,
        iterations: int = 1,
        executor: Optional[
            Callable[[Any], Any]
        ] = None,
        evaluator: Optional[
            Callable[[Any], float]
        ] = None,
    ):

        if iterations <= 0:

            raise ValueError(
                "iterations must be > 0"
            )

        results = []

        for iteration in range(
            1,
            iterations + 1,
        ):

            context, record, _ = (
                self.jager.execute(
                    experiment_id=
                        experiment_id,
                    iteration=iteration,
                    action=action,
                )
            )

            try:

                output = (
                    executor(action)
                    if executor
                    else None
                )

                execution = (
                    self.jager.complete(
                        record,
                        output=output,
                    )
                )

                score = (
                    evaluator(output)
                    if evaluator
                    and output is not None
                    else None
                )

                decision = (
                    self.jager.evaluate(
                        experiment_id=
                            experiment_id,
                        iteration=iteration,
                        score=score,
                    )
                )

                results.append(
                    {
                        "iteration":
                            iteration,
                        "context":
                            context,
                        "execution":
                            execution.to_dict(),
                        "score":
                            score,
                        "decision":
                            decision,
                    }
                )

                if decision.should_stop:

                    break

            except Exception as exc:

                self.jager.complete(
                    record,
                    output=None,
                )

                decision = (
                    self.jager.evaluate(
                        experiment_id=
                            experiment_id,
                        iteration=iteration,
                        error=str(exc),
                    )
                )

                results.append(
                    {
                        "iteration":
                            iteration,
                        "error":
                            str(exc),
                        "decision":
                            decision,
                    }
                )

                if decision.should_stop:

                    break

        return results
