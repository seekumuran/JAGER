from abc import ABC, abstractmethod
from typing import List, Optional

from ..experience.experience_record import (
    ExperienceRecord,
)


class ExperienceRepository(ABC):

    @abstractmethod
    def add(
        self,
        experience: ExperienceRecord,
    ):
        pass

    @abstractmethod
    def get(
        self,
        experience_id: str,
    ) -> Optional[ExperienceRecord]:
        pass

    @abstractmethod
    def all(self) -> List[ExperienceRecord]:
        pass

    @abstractmethod
    def for_target(
        self,
        target: str,
    ) -> List[ExperienceRecord]:
        pass

    @abstractmethod
    def clear(self):
        pass
