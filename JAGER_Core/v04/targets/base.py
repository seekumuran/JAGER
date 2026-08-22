from abc import ABC, abstractmethod
from typing import Dict, Any


class Target(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def observe(self) -> Dict[str, Any]:
        pass
