from abc import ABC, abstractmethod
from typing import Any, Dict


class Target(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def observe(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def execute(
        self,
        action_type: str,
        parameters: Dict[str, Any],
    ) -> Any:
        pass

    def health(self) -> Dict[str, Any]:

        return {
            "target": self.name,
            "healthy": True,
        }
