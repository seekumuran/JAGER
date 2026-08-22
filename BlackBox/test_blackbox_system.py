"""
test_blackbox_system.py

Small test suite for the SimulatedSystem black box.

Run with:
    python3 -m unittest test_blackbox_system.py
or simply:
    python3 test_blackbox_system.py
"""

import unittest

from blackbox_system import (
    SimulatedSystem,
    STATUS_NORMAL,
    STATUS_DEGRADED,
    STATUS_FAILED,
)


class TestSimulatedSystem(unittest.TestCase):
    def test_returns_only_expected_top_level_keys(self):
        system = SimulatedSystem(seed=1)
        result = system.observe(
            cpu_load=10, memory_load=10, num_processes=5, num_threads=5, ipc_intensity=5
        )
        self.assertEqual(set(result.keys()), {"inputs", "telemetry", "status"})

    def test_telemetry_has_expected_fields_only(self):
        system = SimulatedSystem(seed=1)
        result = system.observe(
            cpu_load=10, memory_load=10, num_processes=5, num_threads=5, ipc_intensity=5
        )
        expected_fields = {
            "cpu_usage",
            "memory_usage",
            "latency_ms",
            "process_count",
            "thread_count",
            "ipc_activity",
        }
        self.assertEqual(set(result["telemetry"].keys()), expected_fields)

    def test_status_is_one_of_the_three_valid_values(self):
        system = SimulatedSystem(seed=2)
        result = system.observe(
            cpu_load=50, memory_load=50, num_processes=50, num_threads=50, ipc_intensity=50
        )
        self.assertIn(result["status"], {STATUS_NORMAL, STATUS_DEGRADED, STATUS_FAILED})

    def test_same_seed_same_inputs_are_reproducible(self):
        result_a = SimulatedSystem(seed=99).observe(
            cpu_load=70, memory_load=70, num_processes=100, num_threads=180, ipc_intensity=80
        )
        result_b = SimulatedSystem(seed=99).observe(
            cpu_load=70, memory_load=70, num_processes=100, num_threads=180, ipc_intensity=80
        )
        self.assertEqual(result_a, result_b)

    def test_different_seeds_can_produce_different_telemetry(self):
        result_a = SimulatedSystem(seed=1).observe(
            cpu_load=50, memory_load=50, num_processes=50, num_threads=50, ipc_intensity=50
        )
        result_b = SimulatedSystem(seed=2).observe(
            cpu_load=50, memory_load=50, num_processes=50, num_threads=50, ipc_intensity=50
        )
        self.assertNotEqual(result_a["telemetry"], result_b["telemetry"])

    def test_no_internal_fault_details_are_leaked(self):
        system = SimulatedSystem(seed=7)
        result = system.observe(
            cpu_load=80, memory_load=80, num_processes=100, num_threads=200, ipc_intensity=90
        )
        forbidden_substrings = ["fault", "hidden", "reason", "cause", "contention", "threshold"]
        flat_repr = str(result).lower()
        for term in forbidden_substrings:
            self.assertNotIn(term, flat_repr)

    def test_extreme_load_can_reach_failed_or_degraded(self):
        system = SimulatedSystem(seed=3)
        result = system.observe(
            cpu_load=95, memory_load=95, num_processes=200, num_threads=500, ipc_intensity=95
        )
        self.assertIn(result["status"], {STATUS_DEGRADED, STATUS_FAILED})

    def test_light_load_stays_normal(self):
        system = SimulatedSystem(seed=4)
        result = system.observe(
            cpu_load=5, memory_load=5, num_processes=5, num_threads=5, ipc_intensity=5
        )
        self.assertEqual(result["status"], STATUS_NORMAL)


if __name__ == "__main__":
    unittest.main()
