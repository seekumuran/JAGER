import unittest

from .runtime_diagnostics import (
    RuntimeDiagnostics,
)

from .runtime_observer import (
    RuntimeObserver,
)


class TestRuntimeDiagnostics(
    unittest.TestCase
):

    def test_report(self):

        observer = RuntimeObserver()

        observer.experiment_started(
            "exp-001"
        )

        diagnostics = (
            RuntimeDiagnostics(
                observer
            )
        )

        report = diagnostics.report()

        self.assertEqual(
            report["event_count"],
            1,
        )

        self.assertIn(
            "metrics",
            report,
        )

        self.assertIn(
            "events",
            report,
        )

        self.assertIn(
            "traces",
            report,
        )


if __name__ == "__main__":
    unittest.main()
