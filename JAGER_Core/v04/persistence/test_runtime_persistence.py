import tempfile
import unittest
from pathlib import Path

from ..state.runtime_state import (
    RuntimeState,
)

from .json_runtime_state_repository import (
    JsonRuntimeStateRepository,
)

from .persistent_state_manager import (
    PersistentStateManager,
)


class TestRuntimePersistence(
    unittest.TestCase
):

    def test_state_roundtrip(self):

        with tempfile.TemporaryDirectory() as tmp:

            path = Path(tmp) / "state.json"

            repository = (
                JsonRuntimeStateRepository(
                    str(path)
                )
            )

            state = RuntimeState()

            state.start_experiment(
                "exp-001"
            )

            state.record_discovery()

            state.record_experience()

            state.record_event(
                "test",
                {"value": 1},
            )

            repository.save(state)

            restored = repository.load()

            self.assertIsNotNone(
                restored
            )

            self.assertEqual(
                restored.iteration,
                1,
            )

            self.assertEqual(
                restored.active_experiment_id,
                "exp-001",
            )

            self.assertEqual(
                restored.discoveries_found,
                1,
            )

            self.assertEqual(
                restored.experiences_created,
                1,
            )

            self.assertEqual(
                len(restored.history),
                1,
            )

    def test_manager_survives_restart(self):

        with tempfile.TemporaryDirectory() as tmp:

            path = Path(tmp) / "state.json"

            repository = (
                JsonRuntimeStateRepository(
                    str(path)
                )
            )

            manager = (
                PersistentStateManager(
                    repository
                )
            )

            manager.begin(
                "exp-001"
            )

            manager.event(
                "started"
            )

            # Simulate a process restart.
            new_repository = (
                JsonRuntimeStateRepository(
                    str(path)
                )
            )

            restarted = (
                PersistentStateManager(
                    new_repository
                )
            )

            snapshot = (
                restarted.snapshot()
            )

            self.assertEqual(
                snapshot[
                    "active_experiment_id"
                ],
                "exp-001",
            )

            self.assertEqual(
                snapshot["iteration"],
                1,
            )

            self.assertEqual(
                len(snapshot["history"]),
                1,
            )

    def test_clear(self):

        with tempfile.TemporaryDirectory() as tmp:

            path = Path(tmp) / "state.json"

            repository = (
                JsonRuntimeStateRepository(
                    str(path)
                )
            )

            repository.save(
                RuntimeState()
            )

            self.assertTrue(
                path.exists()
            )

            repository.clear()

            self.assertFalse(
                path.exists()
            )


if __name__ == "__main__":
    unittest.main()
