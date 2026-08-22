import random
import time
from typing import Dict, Any

from .models import Action, Observation


class SimulatedTarget:
    """
    Self-contained synthetic target.

    The failure condition intentionally depends on
    an interaction between multiple variables.
    """

    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)
        self.counter = 0

    def execute(self, action: Action) -> Observation:
        self.counter += 1

        p = action.parameters

        cpu = float(p["cpu_load"])
        memory = float(p["memory_load"])
        processes = int(p["num_processes"])
        threads = int(p["num_threads"])
        ipc = float(p["ipc_intensity"])

        interaction = (
            cpu * 0.30
            + memory * 0.25
            + ipc * 0.25
            + min(processes / 2.0, 100)
            * 0.10
            + min(threads / 4.0, 100)
            * 0.10
        )

        noise = self.rng.uniform(-4.0, 4.0)
        score = interaction + noise

        if (
            cpu > 65
            and memory > 60
            and ipc > 70
            and processes > 90
            and threads > 170
        ):
            status = "FAILED"
        elif score >= 70:
            status = "DEGRADED"
        else:
            status = "NORMAL"

        telemetry = {
            "cpu_usage": round(cpu + noise, 2),
            "memory_usage": round(memory + noise / 2, 2),
            "latency_ms": round(max(1.0, score * 1.8), 2),
            "process_count": processes,
            "thread_count": threads,
            "ipc_activity": round(ipc, 2),
        }

        return Observation(
            observation_id=f"obs-{self.counter:06d}",
            action_id=action.action_id,
            telemetry=telemetry,
            status=status,
            timestamp=time.time(),
        )
