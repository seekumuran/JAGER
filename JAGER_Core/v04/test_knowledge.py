import unittest

from .knowledge import KnowledgeBase
from .knowledge_update import (
    KnowledgeUpdater,
)


class TestKnowledge(unittest.TestCase):

    def test_add_knowledge(self):
        knowledge = KnowledgeBase()

        knowledge.add(
            key="failure",
            pattern="failure_region",
            evidence={
                "status": "FAILED"
            },
            confidence=0.8,
        )

        self.assertEqual(
            len(knowledge),
            1,
        )

    def test_update_knowledge(self):
        updater = KnowledgeUpdater()

        inputs = {
            "cpu_load": 80,
            "memory_load": 80,
            "num_processes": 100,
            "num_threads": 200,
            "ipc_intensity": 80,
        }

        updater.update(
            inputs,
            "FAILED",
            0.9,
        )

        updater.update(
            inputs,
            "FAILED",
            0.95,
        )

        self.assertEqual(
            len(updater.knowledge),
            1,
        )

        entry = updater.knowledge.all()[0]

        self.assertEqual(
            entry.observations,
            2,
        )

    def test_normal_and_failure_are_distinct(self):
        updater = KnowledgeUpdater()

        normal = {
            "cpu_load": 20,
            "memory_load": 20,
            "num_processes": 10,
            "num_threads": 20,
            "ipc_intensity": 20,
        }

        failure = {
            "cpu_load": 80,
            "memory_load": 80,
            "num_processes": 100,
            "num_threads": 200,
            "ipc_intensity": 80,
        }

        updater.update(
            normal,
            "NORMAL",
            0.5,
        )

        updater.update(
            failure,
            "FAILED",
            0.9,
        )

        self.assertEqual(
            len(updater.knowledge),
            2,
        )


if __name__ == "__main__":
    unittest.main()
