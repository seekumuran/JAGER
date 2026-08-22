import unittest

from .config import JagerConfig
from .memory import ExperienceMemory
from .metrics import Metrics
from .policy import SecurityPolicy
from .models import Action


class TestJagerCore(unittest.TestCase):

    def test_memory_starts_empty(self):
        memory = ExperienceMemory()
        self.assertEqual(len(memory), 0)

    def test_metrics_start_zero(self):
        metrics = Metrics()
        self.assertEqual(
            metrics.snapshot()["experiments"],
            0,
        )

    def test_policy_allows_normal_probe(self):
        policy = SecurityPolicy()

        action = Action(
            action_id="test-1",
            operation="probe",
            parameters={
                "cpu_load": 50,
                "memory_load": 50,
                "num_processes": 50,
                "num_threads": 100,
                "ipc_intensity": 50,
            },
        )

        decision = policy.evaluate(action)

        self.assertTrue(decision.allowed)

    def test_policy_blocks_extreme_resources(self):
        policy = SecurityPolicy()

        action = Action(
            action_id="test-2",
            operation="execute",
            parameters={
                "cpu_load": 90,
                "memory_load": 90,
                "num_processes": 200,
                "num_threads": 400,
                "ipc_intensity": 90,
            },
        )

        decision = policy.evaluate(action)

        self.assertFalse(decision.allowed)

    def test_config(self):
        config = JagerConfig()

        self.assertEqual(config.seed, 42)
        self.assertGreater(config.budget, 0)


if __name__ == "__main__":
    unittest.main()
