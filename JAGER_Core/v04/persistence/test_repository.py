import tempfile
import unittest
from pathlib import Path

from ..experience.experience_record import (
    ExperienceRecord,
)

from .memory_experience_repository import (
    MemoryExperienceRepository,
)

from .json_experience_repository import (
    JsonExperienceRepository,
)

from .repository_factory import (
    create_experience_repository,
)


class TestRepositories(
    unittest.TestCase
):

    def _experience(self):

        return ExperienceRecord.create(
            target="mock",
            hypothesis="Test hypothesis",
            action={
                "type": "probe"
            },
            outcome={
                "status": "success"
            },
            discovery=True,
            novelty=0.8,
            confidence=0.9,
            tags=[
                "test"
            ],
        )

    def test_memory_repository(self):

        repository = (
            MemoryExperienceRepository()
        )

        experience = self._experience()

        repository.add(
            experience
        )

        self.assertEqual(
            repository.size(),
            1,
        )

        self.assertEqual(
            repository.get(
                experience.experience_id
            ),
            experience,
        )

        self.assertEqual(
            len(
                repository.for_target(
                    "mock"
                )
            ),
            1,
        )

    def test_json_repository_roundtrip(self):

        with tempfile.TemporaryDirectory() as tmp:

            path = Path(tmp) / (
                "experiences.json"
            )

            repository = (
                JsonExperienceRepository(
                    str(path)
                )
            )

            experience = (
                self._experience()
            )

            repository.add(
                experience
            )

            restored = (
                JsonExperienceRepository(
                    str(path)
                )
            )

            loaded = restored.get(
                experience.experience_id
            )

            self.assertIsNotNone(
                loaded
            )

            self.assertEqual(
                loaded.experience_id,
                experience.experience_id,
            )

            self.assertEqual(
                loaded.target,
                experience.target,
            )

    def test_factory(self):

        memory = (
            create_experience_repository(
                backend="memory"
            )
        )

        self.assertIsInstance(
            memory,
            MemoryExperienceRepository,
        )

        with tempfile.TemporaryDirectory() as tmp:

            repository = (
                create_experience_repository(
                    backend="json",
                    path=str(
                        Path(tmp)
                        / "store.json"
                    ),
                )
            )

            self.assertIsInstance(
                repository,
                JsonExperienceRepository,
            )


if __name__ == "__main__":
    unittest.main()
