import tempfile
import unittest
from pathlib import Path

from .store import ExperimentMemory


class TestExperimentMemory(
    unittest.TestCase
):

    def make_result(
        self,
        target="blackbox",
        status="NORMAL",
    ):

        return {
            "experiment_id": "exp-test",
            "target_name": target,
            "action": {
                "type": "probe"
            },
            "observation": {
                "status": status,
                "telemetry": {},
            },
            "reward": 0.0,
            "novelty": 1.0,
        }

    def test_add_and_get(self):

        with tempfile.TemporaryDirectory() as directory:

            path = (
                Path(directory)
                / "memory.json"
            )

            memory = ExperimentMemory(
                path
            )

            memory.add(
                self.make_result()
            )

            result = memory.get(1)

            self.assertIsNotNone(
                result
            )

            self.assertEqual(
                result["target_name"],
                "blackbox",
            )

    def test_recent(self):

        memory = ExperimentMemory(
            "memory-test.json"
        )

        try:

            memory.add(
                self.make_result()
            )

            memory.add(
                self.make_result(
                    status="DEGRADED"
                )
            )

            recent = memory.recent(1)

            self.assertEqual(
                len(recent),
                1,
            )

            self.assertEqual(
                recent[0][
                    "observation"
                ]["status"],
                "DEGRADED",
            )

        finally:

            memory.clear()

    def test_search(self):

        memory = ExperimentMemory(
            "memory-test.json"
        )

        try:

            memory.add(
                self.make_result(
                    target="blackbox",
                    status="NORMAL",
                )
            )

            memory.add(
                self.make_result(
                    target="linux",
                    status="FAILED",
                )
            )

            results = memory.search(
                target_name="linux",
                status="FAILED",
            )

            self.assertEqual(
                len(results),
                1,
            )

        finally:

            memory.clear()

    def test_persistence(self):

        with tempfile.TemporaryDirectory() as directory:

            path = (
                Path(directory)
                / "memory.json"
            )

            first = ExperimentMemory(
                path
            )

            first.add(
                self.make_result()
            )

            first.save()

            second = ExperimentMemory(
                path
            )

            self.assertEqual(
                len(second.all()),
                1,
            )


if __name__ == "__main__":
    unittest.main()
