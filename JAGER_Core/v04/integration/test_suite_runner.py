import subprocess
import sys
from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class TestRunResult:

    return_code: int
    passed: bool
    output: str
    error: str = ""


class TestSuiteRunner:

    def __init__(
        self,
        package: str = "JAGER_Core.v04",
    ):

        self.package = package

    def run(
        self,
        pattern: Optional[str] = None,
    ) -> TestRunResult:

        command: List[str] = [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            self.package.replace(".", "/"),
        ]

        if pattern:
            command.extend(
                [
                    "-p",
                    pattern,
                ]
            )

        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        return TestRunResult(
            return_code=process.returncode,
            passed=(
                process.returncode == 0
            ),
            output=process.stdout,
            error=process.stderr,
        )

    def passed(self):

        return self.run().passed
