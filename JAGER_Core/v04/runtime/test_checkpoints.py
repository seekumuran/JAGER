import tempfile
import unittest

from .checkpoint import (
    RuntimeCheckpoint,
)

from .checkpoint_manager import (
    CheckpointManager,
)

from .checkpoint_store import (
    CheckpointStore,
)


class TestCheckpoints(
    unittest.TestCase
):

    def test_checkpoint_roundtrip(self):

        with tempfile.TemporaryDirectory() as tmp:

            store = CheckpointStore(
                tmp
            )

            checkpoint = (
                RuntimeCheckpoint(
                    checkpoint_id="cp-001",
                    iteration=5,
                    status="running",
                    experiment_id="exp-001",
                    state={
                        "score": 0.91
                    },
                )
            )

            store.save(
                checkpoint
            )

            restored = store.load(
                "cp-001"
            )

            self.assertIsNotNone(
                restored
            )

            self.assertEqual(
                restored.iteration,
                5,
            )

            self.assertEqual(
                restored.state[
                    "score"
                ],
                0.91,
            )

    def test_manager_latest(self):

        with tempfile.TemporaryDirectory() as tmp:

            manager = CheckpointManager(
                CheckpointStore(tmp)
            )

            manager.create(
                checkpoint_id="cp-001",
                iteration=1,
                status="running",
                state={
                    "step": 1
                },
            )

            manager.create(
                checkpoint_id="cp-002",
                iteration=4,
                status="running",
                state={
                    "step": 4
                },
            )

            latest = manager.latest()

            self.assertEqual(
                latest.checkpoint_id,
                "cp-002",
            )

            self.assertEqual(
                latest.iteration,
                4,
            )

    def test_delete(self):

        with tempfile.TemporaryDirectory() as tmp:

            store = CheckpointStore(
                tmp
            )

            store.save(
                RuntimeCheckpoint(
                    checkpoint_id="cp-001",
                    iteration=1,
                    status="complete",
                )
            )

            self.assertTrue(
                store.exists("cp-001")
            )

            store.delete(
                "cp-001"
            )

            self.assertFalse(
                store.exists("cp-001")
            )


if __name__ == "__main__":
    unittest.main()
