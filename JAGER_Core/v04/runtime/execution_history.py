from typing import List, Optional

from .execution_record import (
    ExecutionRecord,
)


class ExecutionHistory:

    def __init__(self):

        self._records: List[
            ExecutionRecord
        ] = []

    def add(
        self,
        record: ExecutionRecord,
    ):

        self._records.append(
            record
        )

    def get(
        self,
        execution_id: str,
    ) -> Optional[
        ExecutionRecord
    ]:

        for record in self._records:

            if (
                record.execution_id
                == execution_id
            ):
                return record

        return None

    def latest(self):

        if not self._records:

            return None

        return self._records[-1]

    def all(self):

        return list(
            self._records
        )

    def count(self):

        return len(
            self._records
        )

    def successful(self):

        return [
            record
            for record in self._records
            if record.status
            == "completed"
        ]

    def failed(self):

        return [
            record
            for record in self._records
            if record.status
            == "failed"
        ]

    def clear(self):

        self._records.clear()

    def snapshot(self):

        return [
            record.to_dict()
            for record
            in self._records
        ]
