import unittest

from .hunter import JagerHunter


class FakeTarget:

    def observe(self, **inputs):
        cpu = inputs["cpu_load"]
        memory = inputs["memory_load"]

        if (
            cpu > 85
            and memory > 85
        ):
            status = "FAILED"
        elif (
            cpu > 70
            or memory > 70
        ):
            status = "DEGRADED"
        else:
            status = "NORMAL"

        return {
            "inputs": inputs,
            "telemetry": {
                "cpu_usage": cpu,
                "memory_usage": memory,
                "latency_ms": 10,
                "process_count":
                    inputs["num_processes"],
                "thread_count":
                    inputs["num_threads"],
                "ipc_activity":
                    inputs["ipc_intensity"],
            },
            "status": status,
        }


class TestHunterTarget(unittest.TestCase):

    def test_target_is_required(self):
        hunter = JagerHunter(
            seed=42,
            budget=1,
        )

        with self.assertRaises(
            RuntimeError
        ):
            hunter.run()

    def test_hunter_can_use_target(self):
        hunter = JagerHunter(
            seed=42,
            budget=5,
            target=FakeTarget(),
        )

        hunter.run()

        self.assertEqual(
            len(hunter.experiments),
            5,
        )

    def test_reproducible_run(self):
        first = JagerHunter(
            seed=42,
            budget=10,
            target=FakeTarget(),
        )

        second = JagerHunter(
            seed=42,
            budget=10,
            target=FakeTarget(),
        )

        first.run()
        second.run()

        first_inputs = [
            item["action"].parameters
            for item in first.experiments
        ]

        second_inputs = [
            item["action"].parameters
            for item in second.experiments
        ]

        self.assertEqual(
            first_inputs,
            second_inputs,
        )


if __name__ == "__main__":
    unittest.main()
