import os
import time
from typing import Dict, Any


class LinuxTarget:

    name = "linux"

    def __init__(self):
        self.pid = os.getpid()

    def observe(self) -> Dict[str, Any]:

        start = time.perf_counter()

        cpu_usage = self._cpu_usage()
        memory_usage = self._memory_usage()
        process_count = self._process_count()
        thread_count = self._thread_count()

        latency_ms = (
            time.perf_counter() - start
        ) * 1000.0

        status = self._classify(
            cpu_usage,
            memory_usage,
            process_count,
            thread_count,
        )

        return {
            "inputs": {},
            "telemetry": {
                "cpu_usage": cpu_usage,
                "memory_usage": memory_usage,
                "process_count": process_count,
                "thread_count": thread_count,
                "latency_ms": latency_ms,
            },
            "status": status,
        }

    def _cpu_usage(self) -> float:

        try:
            with open(
                "/proc/loadavg",
                "r",
                encoding="utf-8",
            ) as handle:
                load = float(
                    handle.read()
                    .split()[0]
                )

            cpu_count = os.cpu_count() or 1

            return min(
                100.0,
                (load / cpu_count) * 100.0,
            )

        except (
            FileNotFoundError,
            ValueError,
            OSError,
        ):
            return 0.0

    def _memory_usage(self) -> float:

        try:
            values = {}

            with open(
                "/proc/meminfo",
                "r",
                encoding="utf-8",
            ) as handle:

                for line in handle:

                    key, value = (
                        line.split(":", 1)
                    )

                    values[key] = float(
                        value.strip()
                        .split()[0]
                    )

            total = values.get(
                "MemTotal",
                0.0,
            )

            available = values.get(
                "MemAvailable",
                0.0,
            )

            if total <= 0:
                return 0.0

            return (
                (total - available)
                / total
                * 100.0
            )

        except (
            FileNotFoundError,
            ValueError,
            OSError,
        ):
            return 0.0

    def _process_count(self) -> int:

        try:
            return sum(
                name.isdigit()
                for name in os.listdir(
                    "/proc"
                )
            )

        except OSError:
            return 0

    def _thread_count(self) -> int:

        total = 0

        try:

            for name in os.listdir(
                "/proc"
            ):

                if not name.isdigit():
                    continue

                task_dir = (
                    f"/proc/{name}/task"
                )

                try:
                    total += len(
                        os.listdir(
                            task_dir
                        )
                    )

                except OSError:
                    continue

        except OSError:
            pass

        return total

    @staticmethod
    def _classify(
        cpu_usage,
        memory_usage,
        process_count,
        thread_count,
    ):

        if (
            cpu_usage >= 95.0
            or memory_usage >= 95.0
        ):
            return "FAILED"

        if (
            cpu_usage >= 80.0
            or memory_usage >= 80.0
            or process_count >= 1000
            or thread_count >= 5000
        ):
            return "DEGRADED"

        return "NORMAL"
