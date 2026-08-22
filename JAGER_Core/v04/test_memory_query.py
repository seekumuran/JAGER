import unittest

from .experience import (
    Experience,
    ExperienceStore,
)
from .models import (
    Action,
    Observation,
)
from .memory_query import MemoryQuery


class TestMemoryQuery(unittest.TestCase):

    def experience(self, status):
        action = Action(
            action_id="a1",
            operation="probe",
            parameters={
                "cpu_load": 50,
                "memory_load": 50,
                "num_processes": 50,
                "num_threads": 100,
                "ipc_intensity": 50,
            },
        )

        observation = Observation(
            observation_id="o1",
            action_id="a1",
            telemetry={},
            status=status,
            timestamp=0,
        )

        return Experience(
            observation_id="o1",
            action=action,
            observation=observation,
            reward=10.0,
            novelty=1.0,
            useful=True,
        )

    def test_nearest(self):
        memory = ExperienceStore()

        memory.add(
            self.experience("FAILED")
        )

        query = MemoryQuery(memory)

        result = query.nearest(
            {
                "cpu_load": 50,
                "memory_load": 50,
                "num_processes": 50,
                "num_threads": 100,
                "ipc_intensity": 50,
            }
        )

        self.assertEqual(
            len(result),
            1,
        )

    def test_nearby_failure(self):
        memory = ExperienceStore()

        memory.add(
            self.experience("FAILED")
        )

        query = MemoryQuery(memory)

        result = query.failures_near(
            {
                "cpu_load": 50,
                "memory_load": 50,
                "num_processes": 50,
                "num_threads": 100,
                "ipc_intensity": 50,
            }
        )

        self.assertEqual(
            len(result),
            1,
        )


if __name__ == "__main__":
    unittest.main()
