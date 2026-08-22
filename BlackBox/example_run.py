"""
example_run.py

Runs 10 experiments against the SimulatedSystem black box and prints the
inputs, telemetry, and status for each. This is the first black-box target
for JAGER (or any other test harness) to be pointed at.

Run with:
    python3 example_run.py
"""

from blackbox_system import SimulatedSystem


def main() -> None:
    system = SimulatedSystem(seed=42)

    experiments = [
        dict(cpu_load=10, memory_load=15, num_processes=20, num_threads=10, ipc_intensity=5),
        dict(cpu_load=40, memory_load=35, num_processes=50, num_threads=60, ipc_intensity=20),
        dict(cpu_load=60, memory_load=55, num_processes=80, num_threads=120, ipc_intensity=40),
        dict(cpu_load=70, memory_load=70, num_processes=100, num_threads=180, ipc_intensity=80),
        dict(cpu_load=20, memory_load=90, num_processes=30, num_threads=200, ipc_intensity=85),
        dict(cpu_load=90, memory_load=20, num_processes=10, num_threads=300, ipc_intensity=90),
        dict(cpu_load=75, memory_load=75, num_processes=60, num_threads=250, ipc_intensity=90),
        dict(cpu_load=95, memory_load=95, num_processes=200, num_threads=500, ipc_intensity=95),
        dict(cpu_load=5, memory_load=5, num_processes=5, num_threads=5, ipc_intensity=5),
        dict(cpu_load=50, memory_load=50, num_processes=50, num_threads=50, ipc_intensity=50),
    ]

    for i, params in enumerate(experiments, start=1):
        result = system.observe(**params)
        print(f"--- Experiment {i} ---")
        print(f"  inputs:    {result['inputs']}")
        print(f"  telemetry: {result['telemetry']}")
        print(f"  status:    {result['status']}")
        print()


if __name__ == "__main__":
    main()
