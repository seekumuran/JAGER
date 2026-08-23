from dataclasses import dataclass
from typing import Callable, List


@dataclass(frozen=True)
class AuditResult:

    name: str
    passed: bool
    message: str


class FinalAudit:

    def __init__(self):

        self._checks: List[
            Callable[[], AuditResult]
        ] = []

    def register(
        self,
        name: str,
        check: Callable[[], bool],
    ):

        def wrapped():

            try:

                passed = bool(check())

                return AuditResult(
                    name=name,
                    passed=passed,
                    message=(
                        "passed"
                        if passed
                        else "failed"
                    ),
                )

            except Exception as exc:

                return AuditResult(
                    name=name,
                    passed=False,
                    message=str(exc),
                )

        self._checks.append(
            wrapped
        )

    def run(self):

        return [
            check()
            for check in self._checks
        ]

    def passed(self):

        results = self.run()

        return all(
            result.passed
            for result in results
        )

    def summary(self):

        results = self.run()

        return {
            "passed":
                sum(
                    result.passed
                    for result in results
                ),

            "failed":
                sum(
                    not result.passed
                    for result in results
                ),

            "total":
                len(results),

            "healthy":
                all(
                    result.passed
                    for result in results
                ),
        }
