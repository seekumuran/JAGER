from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Telemetry:
    cpu_usage: float
    memory_usage: float
    latency_ms: float
    process_count: int
    thread_count: int
    ipc_activity: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cpu_usage": self.cpu_usage,
            "memory_usage": self.memory_usage,
            "latency_ms": self.latency_ms,
            "process_count": self.process_count,
            "thread_count": self.thread_count,
            "ipc_activity": self.ipc_activity,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            cpu_usage=float(data["cpu_usage"]),
            memory_usage=float(data["memory_usage"]),
            latency_ms=float(data["latency_ms"]),
            process_count=int(data["process_count"]),
            thread_count=int(data["thread_count"]),
            ipc_activity=float(data["ipc_activity"]),
        )
