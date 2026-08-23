from abc import ABC, abstractmethod
from typing import Optional

from ..state.runtime_state import RuntimeState


class RuntimeStateRepository(ABC):

    @abstractmethod
    def save(
        self,
        state: RuntimeState,
    ):
        pass

    @abstractmethod
    def load(self) -> Optional[RuntimeState]:
        pass

    @abstractmethod
    def clear(self):
        pass
