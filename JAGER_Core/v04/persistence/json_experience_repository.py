import json
from pathlib import Path
from typing import List, Optional

from ..experience.experience_record import (
    ExperienceRecord,
)

from .experience_repository import (
    ExperienceRepository,
)


class JsonExperienceRepository(
    ExperienceRepository
):

    def __init__(
        self,
        path: str,
        maximum_size: int = 10000,
    ):

        self.path = Path(path)

        self.maximum_size = (
            maximum_size
        )

        self._records = {}

        self._load()

    def add(
        self,
        experience: ExperienceRecord,
    ):

        self._records[
            experience.experience_id
        ] = experience

        self._trim()

        self._save()

        return experience

    def get(
        self,
        experience_id: str,
    ) -> Optional[
        ExperienceRecord
    ]:

        return self._records.get(
            experience_id
        )

    def all(
        self,
    ) -> List[ExperienceRecord]:

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

        self._save()

    def size(self):

        return len(self._records)

    def _load(self):

        if not self.path.exists():
            return

        with self.path.open(
            "r",
            encoding="utf-8",
        ) as handle:

            data = json.load(handle)

        if not isinstance(data, list):
            raise ValueError(
                "Experience repository "
                "must contain a JSON list"
            )

        for item in data:

            experience = (
                ExperienceRecord.from_dict(
                    item
                )
            )

            self._records[
                experience.experience_id
            ] = experience

    def _save(self):

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        data = [
            record.to_dict()
            for record
            in self._records.values()
        ]

        temporary = self.path.with_suffix(
            self.path.suffix + ".tmp"
        )

        with temporary.open(
            "w",
            encoding="utf-8",
        ) as handle:

            json.dump(
                data,
                handle,
                indent=2,
            )

        temporary.replace(
            self.path
        )

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
