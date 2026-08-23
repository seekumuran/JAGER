from typing import Dict, List, Optional

from ..experience.experience_record import (
    ExperienceRecord,
)

from .experience_repository import (
    ExperienceRepository,
)


class MemoryExperienceRepository(
    ExperienceRepository
):

    def __init__(
        self,
        maximum_size: int = 10000,
    ):

        if maximum_size <= 0:
            raise ValueError(
                "maximum_size must be positive"
            )

        self.maximum_size = maximum_size

        self._records: Dict[
            str,
            ExperienceRecord,
        ] = {}

    def add(
        self,
        experience: ExperienceRecord,
    ):

        self._records[
            experience.experience_id
        ] = experience

        self._trim()

        return experience

    def get(
        self,
        experience_id: str,
    ):

        return self._records.get(
            experience_id
        )

    def all(self):

        return list(
            self._records.values()
        )

    def for_target(
        self,
        target: str,
    ):

        return [
            record
            for record
            in self._records.values()
            if record.target == target
        ]

    def clear(self):

        self._records.clear()

    def size(self):

        return len(self._records)

    def _trim(self):

        while (
            len(self._records)
            > self.maximum_size
        ):

            oldest = min(
                self._records.values(),
                key=lambda record:
                    record.created_at,
            )

            del self._records[
                oldest.experience_id
            ]
