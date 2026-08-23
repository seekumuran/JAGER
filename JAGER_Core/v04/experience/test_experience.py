import unittest

from .experience_record import (
    ExperienceRecord,
)

from .experience_store import (
    ExperienceStore,
)

from .experience_manager import (
    ExperienceManager,
)


class TestExperience(
    unittest.TestCase
):

    def create_experience(
        self,
        target="blackbox",
        tags=None,
        discovery=False,
    ):

        return ExperienceRecord.create(
            target=target,
            hypothesis="latency may increase",
            action={
                "type": "probe",
                "parameters": {
                    "load": 80
                },
            },
            outcome={
                "latency_ms": 250
            },
            discovery=discovery,
            novelty=0.8,
            confidence=0.9,
            tags=tags or [
                "latency",
                "load",
            ],
        )

    def test_record_creation(self):

        record = self.create_experience()

        self.assertEqual(
            record.target,
            "blackbox",
        )

        self.assertFalse(
            record.discovery
        )

        self.assertTrue(
            record.experience_id
        )

    def test_store(self):

        store = ExperienceStore()

        record = self.create_experience()

        store.add(record)

        self.assertEqual(
            store.size(),
            1,
        )

        self.assertEqual(
            store.get(
                record.experience_id
            ),
            record,
        )

    def test_target_filter(self):

        store = ExperienceStore()

        store.add(
            self.create_experience(
                target="blackbox"
            )
        )

        store.add(
            self.create_experience(
                target="linux"
            )
        )

        self.assertEqual(
            len(
                store.for_target(
                    "blackbox"
                )
            ),
            1,
        )

    def test_discovery_filter(self):

        store = ExperienceStore()

        store.add(
            self.create_experience(
                discovery=True
            )
        )

        store.add(
            self.create_experience(
                discovery=False
            )
        )

        self.assertEqual(
            len(store.discoveries()),
            1,
        )

    def test_retrieval(self):

        manager = ExperienceManager()

        record = self.create_experience(
            tags=["latency", "load"]
        )

        manager.add(record)

        results = manager.retrieve(
            target="blackbox",
            tags=["latency"],
            limit=5,
        )

        self.assertEqual(
            len(results),
            1,
        )

        self.assertEqual(
            results[0].experience_id,
            record.experience_id,
        )

    def test_snapshot(self):

        manager = ExperienceManager()

        manager.add(
            self.create_experience()
        )

        snapshot = manager.snapshot()

        self.assertEqual(
            len(snapshot),
            1,
        )

        self.assertIn(
            "experience_id",
            snapshot[0],
        )


if __name__ == "__main__":
    unittest.main()
