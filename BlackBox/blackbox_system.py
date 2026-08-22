"""
blackbox_system.py

A tiny black-box simulated target for JAGER.

    INPUT -> SIMULATED SYSTEM -> TELEMETRY / OUTCOME

This module simulates a generic computer system that accepts a small set of
load-style inputs and returns only *observable* telemetry plus a coarse
system status (NORMAL / DEGRADED / FAILED).

Design intent
--------------
This is meant to be treated as a genuine black box by anything that later
probes it (a policy-testing harness, an autonomous agent, a "hunter", etc.).
The public API intentionally exposes nothing about *why* a particular status
was produced. Callers get exactly three things back:

    - the inputs they supplied (echoed back for convenience/logging)
    - telemetry values
    - a status label

Nothing else. Do not add fields, exceptions, log lines, or docstrings-at-call-site
that reveal the internal fault model to anything consuming this module's output.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Dict, Union

__all__ = [
    "SimulatedSystem",
    "STATUS_NORMAL",
    "STATUS_DEGRADED",
    "STATUS_FAILED",
]

STATUS_NORMAL = "NORMAL"
STATUS_DEGRADED = "DEGRADED"
STATUS_FAILED = "FAILED"

Number = Union[int, float]


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


@dataclass
class SimulatedSystem:
    """
    A reproducible black-box system simulator.

    Parameters
    ----------
    seed:
        Random seed controlling all internal noise. Two SimulatedSystem
        instances created with the same seed, called with the same inputs
        in the same order, will produce identical results.
    """

    seed: int = 42
    _rng: random.Random = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._rng = random.Random(self.seed)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def observe(
        self,
        cpu_load: Number,
        memory_load: Number,
        num_processes: int,
        num_threads: int,
        ipc_intensity: Number,
    ) -> Dict[str, object]:
        """
        Run one observation of the simulated system.

        cpu_load, memory_load, ipc_intensity: expected on a 0-100 scale.
        num_processes, num_threads: non-negative integers.

        Returns a dict with exactly three top-level keys: "inputs",
        "telemetry", and "status". No internal reasoning is exposed.
        """
        cpu_load = _clamp(float(cpu_load), 0, 100)
        memory_load = _clamp(float(memory_load), 0, 100)
        num_processes = max(0, int(num_processes))
        num_threads = max(0, int(num_threads))
        ipc_intensity = _clamp(float(ipc_intensity), 0, 100)

        telemetry = self._compute_telemetry(
            cpu_load, memory_load, num_processes, num_threads, ipc_intensity
        )
        status = self._compute_status(
            cpu_load, memory_load, num_threads, ipc_intensity, telemetry
        )

        return {
            "inputs": {
                "cpu_load": cpu_load,
                "memory_load": memory_load,
                "num_processes": num_processes,
                "num_threads": num_threads,
                "ipc_intensity": ipc_intensity,
            },
            "telemetry": telemetry,
            "status": status,
        }

    # ------------------------------------------------------------------
    # Internal telemetry model (observable side-effects only)
    # ------------------------------------------------------------------
    def _compute_telemetry(
        self,
        cpu_load: float,
        memory_load: float,
        num_processes: int,
        num_threads: int,
        ipc_intensity: float,
    ) -> Dict[str, object]:
        rng = self._rng

        thread_overhead = min(20.0, num_threads / 100.0)
        cpu_usage = _clamp(cpu_load + thread_overhead + rng.uniform(-3, 3), 0, 100)

        process_overhead = min(15.0, num_processes / 100.0)
        memory_usage = _clamp(memory_load + process_overhead + rng.uniform(-3, 3), 0, 100)

        latency_ms = max(
            0.0,
            5.0
            + cpu_usage * 0.6
            + memory_usage * 0.4
            + ipc_intensity * 0.3
            + num_threads * 0.02
            + rng.uniform(-5, 5),
        )

        process_count = max(0, num_processes + rng.randint(-2, 2))
        thread_count = max(0, num_threads + rng.randint(-5, 5))

        ipc_activity = _clamp(ipc_intensity + rng.uniform(-4, 4), 0, 100)

        return {
            "cpu_usage": round(cpu_usage, 2),
            "memory_usage": round(memory_usage, 2),
            "latency_ms": round(latency_ms, 2),
            "process_count": process_count,
            "thread_count": thread_count,
            "ipc_activity": round(ipc_activity, 2),
        }

    # ------------------------------------------------------------------
    # Internal status / fault model.
    # Everything below this line is deliberately not part of the public
    # contract and must never be surfaced to a caller.
    # ------------------------------------------------------------------
    def _compute_status(
        self,
        cpu_load: float,
        memory_load: float,
        num_threads: int,
        ipc_intensity: float,
        telemetry: Dict[str, object],
    ) -> str:
        if self._hidden_fault_condition(cpu_load, memory_load, num_threads, ipc_intensity):
            return STATUS_FAILED

        if (
            telemetry["cpu_usage"] > 90
            or telemetry["memory_usage"] > 90
            or telemetry["latency_ms"] > 150
        ):
            return STATUS_DEGRADED

        return STATUS_NORMAL

    @staticmethod
    def _hidden_fault_condition(
        cpu_load: float,
        memory_load: float,
        num_threads: int,
        ipc_intensity: float,
    ) -> bool:
        """
        Single hidden failure mode, gated on a *combination* of inputs
        rather than any one threshold. Loosely modeled on a thread/IPC
        contention collapse: a system running a lot of threads that are
        all doing heavy inter-process communication, under already-elevated
        resource pressure, can wedge itself even though no single input
        looks extreme on its own.

        This function's existence, name, and thresholds must never be
        surfaced through the public API.
        """
        threads_high = num_threads > 150
        ipc_high = ipc_intensity > 75
        avg_resource_load = (cpu_load + memory_load) / 2.0
        contention_high = avg_resource_load > 65

        return threads_high and ipc_high and contention_high
