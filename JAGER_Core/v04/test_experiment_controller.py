import unittest

from .experiment_controller import (
    ExperimentController,
)
from .hunter import JagerHunter


class FakeTarget:

    def observe(self, **inputs):
        return {
            "inputs": inputs,
            "telemetry": {
                "cpu_usage":
                    inputs["cpu_load"],
                "memory_usage":
                    inputs["memory_load"],
                "latency_ms": 10,
                "process_count":
                    inputs["num_processes"],
                "thread_count":
                    inputs["num_threads"],
                "ipc_activity":
                    inputs["ipc_intensity"],
            },
            "status": "NORMAL",
        }


class TestExperimentController(
    unittest.TestCase
):

    def make_controller(
        self,
        budget=5,
    ):
        hunter = JagerHunter(
            seed=42,
            budget=budget,
            target=FakeTarget(),
        )

        return ExperimentController(
            hunter
        )

    def test_controller_runs_budget(self):
        controller = self.make_controller(
            budget=5
        )

        results = controller.start()

        self.assertEqual(
            len(results),
            5,
        )

        self.assertEqual(
            len(
                controller.hunter.experiments
            ),
            5,
        )

        self.assertTrue(
            controller.completed
        )

    def test_progress(self):
        controller = self.make_controller(
            budget=10
        )

        controller.start()

        progress = (
            controller.progress()
        )

        self.assertEqual(
            progress["completed"],
            10,
        )

        self.assertEqual(
            progress["budget"],
            10,
        )

        self.assertEqual(
            progress["percentage"],
            100.0,
        )

    def test_stop(self):
        controller = self.make_controller(
            budget=10
        )

        controller.started = True
        controller.stop()

        self.assertTrue(
            controller.stopped
        )


if __name__ == "__main__":
    unittest.main()
