import unittest

from .runtime_observer import (
    RuntimeObserver,
)

from .tracer import (
    RuntimeTracer,
)


class TestRuntimeTracing(
    unittest.TestCase
):

    def test_successful_span(self):

        tracer = RuntimeTracer()

        with tracer.span(
            "planner",
            metadata={
                "iteration": 1
            },
        ):

            value = 2 + 2

        self.assertEqual(
            value,
            4,
        )

        spans = tracer.spans()

        self.assertEqual(
            len(spans),
            1,
        )

        self.assertTrue(
            spans[0].success
        )

        self.assertIsNotNone(
            spans[0].duration_ms
        )

    def test_failed_span(self):

        tracer = RuntimeTracer()

        with self.assertRaises(
            RuntimeError
        ):

            with tracer.span(
                "executor"
            ):

                raise RuntimeError(
                    "execution failed"
                )

        span = tracer.spans()[0]

        self.assertFalse(
            span.success
        )

        self.assertEqual(
            span.error,
            "execution failed",
        )

    def test_runtime_observer(self):

        observer = RuntimeObserver()

        observer.experiment_started(
            "exp-001"
        )

        observer.experiment_completed(
            "exp-001"
        )

        observer.discovery(
            "exp-001",
            {
                "value": 0.91
            },
        )

        snapshot = (
            observer.snapshot()
        )

        counters = (
            snapshot[
                "metrics"
            ][
                "counters"
            ]
        )

        self.assertEqual(
            counters[
                "experiments.started"
            ],
            1,
        )

        self.assertEqual(
            counters[
                "experiments.completed"
            ],
            1,
        )

        self.assertEqual(
            counters[
                "discoveries.found"
            ],
            1,
        )

        self.assertEqual(
            len(snapshot["events"]),
            3,
        )


if __name__ == "__main__":
    unittest.main()
