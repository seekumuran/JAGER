import tempfile
import unittest
from pathlib import Path

from .event import SecurityEvent
from .logger import EventLogger


class TestObservability(
    unittest.TestCase
):

    def test_event_creation(self):

        event = SecurityEvent.create(
            trace_id="trace-001",
            agent="jager",
            target="linux",
            operation="observe",
            resource="system",
            decision="ALLOW",
            reason="Action permitted",
            risk=0.1,
            experiment_id="exp-001",
        )

        data = event.to_dict()

        self.assertEqual(
            data["trace_id"],
            "trace-001",
        )

        self.assertEqual(
            data["decision"],
            "ALLOW",
        )

    def test_event_persistence(self):

        with tempfile.TemporaryDirectory() as directory:

            path = (
                Path(directory)
                / "events.jsonl"
            )

            logger = EventLogger(path)

            event = SecurityEvent.create(
                trace_id="trace-001",
                agent="jager",
                target="linux",
                operation="observe",
                resource="system",
                decision="ALLOW",
                reason="Action permitted",
                risk=0.1,
                experiment_id="exp-001",
            )

            logger.write(event)

            events = logger.read()

            self.assertEqual(
                len(events),
                1,
            )

            self.assertEqual(
                events[0]["trace_id"],
                "trace-001",
            )


if __name__ == "__main__":
    unittest.main()
