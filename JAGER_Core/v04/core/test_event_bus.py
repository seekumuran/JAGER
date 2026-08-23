import unittest

from .event import JagerEvent
from .event_bus import EventBus


class TestEventBus(
    unittest.TestCase
):

    def test_publish(self):

        bus = EventBus()

        received = []

        def handler(event):

            received.append(
                event.payload
            )

        bus.subscribe(
            "test",
            handler,
        )

        bus.publish(
            JagerEvent(
                event_type="test",
                payload={
                    "value": 42
                },
            )
        )

        self.assertEqual(
            len(received),
            1,
        )

        self.assertEqual(
            received[0]["value"],
            42,
        )

    def test_wildcard(self):

        bus = EventBus()

        received = []

        bus.subscribe(
            "*",
            lambda event:
                received.append(event),
        )

        bus.emit(
            "experiment.created"
        )

        self.assertEqual(
            len(received),
            1,
        )

    def test_unsubscribe(self):

        bus = EventBus()

        received = []

        def handler(event):

            received.append(event)

        bus.subscribe(
            "test",
            handler,
        )

        bus.unsubscribe(
            "test",
            handler,
        )

        bus.emit("test")

        self.assertEqual(
            len(received),
            0,
        )


if __name__ == "__main__":

    unittest.main()
