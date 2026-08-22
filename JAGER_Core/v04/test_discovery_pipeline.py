import unittest

from .discovery_pipeline import (
    DiscoveryPipeline,
)
from .hunter import JagerHunter


class FakeTarget:

    def observe(self, **inputs):

        if (
            inputs["cpu_load"] > 90
            and inputs["memory_load"] > 90
        ):
            status = "FAILED"

        else:
            status = "NORMAL"

        return {
            "inputs": inputs,
            "telemetry": {},
            "status": status,
        }


class TestDiscoveryPipeline(
    unittest.TestCase
):

    def test_failed_candidate_is_detected(self):

        target = FakeTarget()

        hunter = JagerHunter(
            seed=42,
            budget=1,
            target=target,
        )

        pipeline = DiscoveryPipeline(
            hunter,
            target,
            verification_attempts=3,
        )

        experiment = {
            "experiment_id":
                "experiment-1",
            "action": type(
                "Action",
                (),
                {
                    "parameters": {
                        "cpu_load": 95,
                        "memory_load": 95,
                        "num_processes": 100,
                        "num_threads": 100,
                        "ipc_intensity": 50,
                    }
                },
            )(),
            "observation": type(
                "Observation",
                (),
                {
                    "status": "FAILED"
                },
            )(),
            "experience": type(
                "Experience",
                (),
                {
                    "novelty": 0.8,
                    "reward": 1.0,
                },
            )(),
        }

        result = pipeline.process(
            experiment
        )

        self.assertIsNotNone(
            result
        )

        self.assertTrue(
            result[
                "verification"
            ]["confirmed"]
        )

        self.assertEqual(
            pipeline.statistics()[
                "candidates"
            ],
            1,
        )

        self.assertEqual(
            pipeline.statistics()[
                "verified"
            ],
            1,
        )


if __name__ == "__main__":
    unittest.main()
