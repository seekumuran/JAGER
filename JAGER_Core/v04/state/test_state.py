import unittest

from .runtime_state import (
    RuntimeState,
)

from .state_store import (
    StateStore,
)

from .state_manager import (
    StateManager,
)


class TestRuntimeState(
    unittest.TestCase
):

    def test_experiment_lifecycle(self):

        state = RuntimeState()

        self.assertEqual(
            state.status,
            "idle",
        )

        state.start_experiment(
            "exp-001"
        )

        self.assertEqual(
            state.status,
            "running",
        )

        self.assertEqual(
            state.iteration,
            1,
        )

        state.complete_experiment(
            "exp-001"
        )

        self.assertEqual(
            state.status,
            "idle",
        )

        self.assertEqual(
            state.experiments_completed,
            1,
        )

    def test_failed_experiment(self):

        state = RuntimeState()

        state.start_experiment(
            "exp-002"
        )

        state.fail_experiment(
            "exp-002"
        )

        self.assertEqual(
            state.experiments_failed,
            1,
        )

    def test_metrics(self):

        state = RuntimeState()

        state.record_discovery()
        state.record_experience()

        self.assertEqual(
            state.discoveries_found,
            1,
        )

        self.assertEqual(
            state.experiences_created,
            1,
        )


class TestStateStore(
    unittest.TestCase
):

    def test_snapshot_isolated(self):

        store = StateStore()

        state = store.get()

        state.iteration = 99

        self.assertEqual(
            store.get().iteration,
            0,
        )

    def test_mutation(self):

        store = StateStore()

        store.mutate(
            lambda state:
                state.start_experiment(
                    "exp-001"
                )
        )

        self.assertEqual(
            store.get()
            .active_experiment_id,
            "exp-001",
        )


class TestStateManager(
    unittest.TestCase
):

    def test_manager(self):

        manager = StateManager()

        manager.begin(
            "exp-001"
        )

        manager.event(
            "experiment_started",
            {
                "experiment_id":
                    "exp-001"
            },
        )

        manager.complete(
            "exp-001"
        )

        snapshot = manager.snapshot()

        self.assertEqual(
            snapshot[
                "experiments_completed"
            ],
            1,
        )

        self.assertEqual(
            len(snapshot["history"]),
            1,
        )

    def test_reset(self):

        manager = StateManager()

        manager.begin(
            "exp-001"
        )

        manager.reset()

        self.assertEqual(
            manager.snapshot()["status"],
            "idle",
        )


if __name__ == "__main__":
    unittest.main()
