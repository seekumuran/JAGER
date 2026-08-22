from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class ActionSpace:
    cpu_min: float = 0.0
    cpu_max: float = 100.0

    memory_min: float = 0.0
    memory_max: float = 100.0

    process_min: int = 0
    process_max: int = 200

    thread_min: int = 0
    thread_max: int = 400

    ipc_min: float = 0.0
    ipc_max: float = 100.0

    def contains(
        self,
        parameters: Dict[str, Any],
    ):
        return (
            self.cpu_min
            <= parameters["cpu_load"]
            <= self.cpu_max
            and
            self.memory_min
            <= parameters["memory_load"]
            <= self.memory_max
            and
            self.process_min
            <= parameters["num_processes"]
            <= self.process_max
            and
            self.thread_min
            <= parameters["num_threads"]
            <= self.thread_max
            and
            self.ipc_min
            <= parameters["ipc_intensity"]
            <= self.ipc_max
        )
