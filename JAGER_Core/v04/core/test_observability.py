import tempfile
import unittest

from .event_manager import EventManager
from .event_store import EventStore
from .observability import Observability
from .telemetry_store import TelemetryStore


class TestObservability(
    unittest.TestCase
):

    def test_metrics_and_events(self):

        with tempfile.TemporaryDirectory() as tmp:

            events = EventManager(
                EventStore(
                    f"{tmp}/events.json"
                )
            )

            observability = Observability(
                events
            )

            observability.metric(
                "score",
                0.75,
                iteration=1,
            )

            observability.event(
                "test.event",
                payload={
                    "metrics": {
                        "latency": 12
                    },
                    "iteration": 1,
                },
            )

            snapshot = (
                observability.snapshot()
            )

            self.assertIn(
                "events",
                snapshot,
            )

            self.assertIn(
                "telemetry",
                snapshot,
            )

            telemetry = (
                snapshot["telemetry"]
            )

            self.assertGreaterEqual(
                telemetry["events_seen"],
                1,
            )

    def test_persistence(self):

        with tempfile.TemporaryDirectory() as tmp:

            events = EventManager()

            observability = Observability(
                events
            )

            observability.metric(
                "score",
                0.9,
            )

            observability.telemetry.store = (
                TelemetryStore(
                    f"{tmp}/telemetry.json"
                )
            )

            observability.persist()

            loaded = (
                observability.telemetry.load()
            )

            self.assertIn(
                "metrics",
                loaded,
            )


if __name__ == "__main__":

    unittest.main()
