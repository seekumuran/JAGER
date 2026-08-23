import tempfile
import unittest

from .event_manager import (
    EventManager,
)

from .event_store import (
    EventStore,
)

from .event_types import (
    EXPERIMENT_CREATED,
)


class TestEventManager(
    unittest.TestCase
):

    def test_event_flow(self):

        with tempfile.TemporaryDirectory() as tmp:

            manager = EventManager(
                EventStore(
                    f"{tmp}/events.json"
                )
            )

            received = []

            manager.subscribe(
                EXPERIMENT_CREATED,
                lambda event:
                    received.append(event),
            )

            manager.emit(
                EXPERIMENT_CREATED,
                payload={
                    "experiment_id":
                        "exp-001"
                },
                source="test",
            )

            self.assertEqual(
                len(received),
                1,
            )

            history = manager.history()

            self.assertEqual(
                len(history),
                1,
            )

            stored = manager.store.load()

            self.assertEqual(
                len(stored),
                1,
            )

            self.assertEqual(
                stored[0]["event_type"],
                EXPERIMENT_CREATED,
            )

    def test_lifecycle_emitter(self):

        manager = EventManager()

        manager.lifecycle.runtime_started()

        self.assertEqual(
            len(manager.history()),
            1,
        )


if __name__ == "__main__":

    unittest.main()
