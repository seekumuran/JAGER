from abc import ABC, abstractmethod
from typing import Any, Dict


class TargetAdapter(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def execute(
        self,
        action_type: str,
        parameters: Dict[str, Any],
    ):
        pass

    def describe(self):

        return {
            "name": self.name,
            "type": (
                self.__class__.__name__
            ),
        }
