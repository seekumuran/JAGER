from pathlib import Path

from .result_writer import ResultWriter
from .result_validator import (
    ResultValidator,
)


class RunManager:

    def __init__(
        self,
        output_directory="runs",
    ):
        self.writer = ResultWriter(
            output_directory
        )

        self.validator = (
            ResultValidator()
        )

    def save(self, run):

        data = run.to_dict()

        self.validator.validate(
            data
        )

        return self.writer.write(
            run
        )

    def load(self, filename):

        data = self.writer.read(
            filename
        )

        self.validator.validate(
            data
        )

        return data

    def list_runs(self):

        directory = (
            self.writer.directory
        )

        return sorted(
            path.name
            for path in directory.glob(
                "*.json"
            )
        )
