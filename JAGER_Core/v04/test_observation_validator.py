import unittest

from .observation_validator import (
    validate_observation,
)
from .errors import InvalidObservationError


class TestObservationValidator(
    unittest.TestCase
):

    def valid(self):
        return {
            "inputs": {
                "cpu_load": 50,
                "memory_load": 50,
                "num_processes": 10,
                "num_threads": 20,
                "ipc_intensity": 50,
            },
            "telemetry": {
                "cpu_usage": 50,
                "memory_usage": 50,
                "latency_ms": 10,
                "process_count": 10,
                "thread_count": 20,
                "ipc_activity": 50,
            },
            "status": "NORMAL",
        }

    def test_valid_observation(self):
        self.assertTrue(
            validate_observation(
                self.valid()
            )
        )

    def test_invalid_status(self):
        data = self.valid()
        data["status"] = "UNKNOWN"

        with self.assertRaises(
            InvalidObservationError
        ):
            validate_observation(data)

    def test_missing_telemetry(self):
        data = self.valid()

        del data["telemetry"]["cpu_usage"]

        with self.assertRaises(
            InvalidObservationError
        ):
            validate_observation(data)


if __name__ == "__main__":
    unittest.main()
