from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class SafetyLimits:
    max_cpu: float = 95.0
    max_memory: float = 95.0
    max_processes: int = 190
    max_threads: int = 380
    max_ipc: float = 95.0


class SafetyController:
    def __init__(self, limits=None):
        self.limits = limits or SafetyLimits()

    def check(self, parameters: Dict[str, Any]):
        violations = []

        if parameters["cpu_load"] > self.limits.max_cpu:
            violations.append("CPU_LIMIT")

        if parameters["memory_load"] > self.limits.max_memory:
            violations.append("MEMORY_LIMIT")

        if parameters["num_processes"] > self.limits.max_processes:
            violations.append("PROCESS_LIMIT")

        if parameters["num_threads"] > self.limits.max_threads:
            violations.append("THREAD_LIMIT")

        if parameters["ipc_intensity"] > self.limits.max_ipc:
            violations.append("IPC_LIMIT")

        return {
            "safe": not violations,
            "violations": violations,
        }
