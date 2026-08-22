import unittest

from .hunter import JagerHunter
from .protocol import ExperimentProtocol
from .protocol_executor import (
    ProtocolExecutor,
)


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


class TestProtocolExecutor(
    unittest.TestCase
):

    def test_protocol_execution(self):

        hunter = JagerHunter(
            seed=42,
            budget=5,
            target=FakeTarget(),
        )

        executor = ProtocolExecutor(
            hunter,
            ExperimentProtocol(),
        )

        result = executor.run()

        self.assertEqual(
            result["state"],
            "FINALIZED",
        )

        self.assertIn(
            "INITIALIZED",
            result["history"],
        )

        self.assertIn(
            "BASELINE",
            result["history"],
        )

        self.assertIn(
            "EXPLORE",
            result["history"],
        )

        self.assertIn(
            "FINALIZED",
            result["history"],
        )


if __name__ == "__main__":
    unittest.main()
