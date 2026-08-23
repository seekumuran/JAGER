import unittest

from .diagnostics import Diagnostics
from .jager import create


class TestDiagnostics(
    unittest.TestCase
):

    def test_snapshot(self):

        jager = create()

        diagnostics = Diagnostics(
            jager
        )

        snapshot = (
            diagnostics.snapshot()
        )

        self.assertIn(
            "version",
            snapshot,
        )

        self.assertIn(
            "runtime",
            snapshot,
        )

    def test_summary(self):

        jager = create()

        summary = Diagnostics(
            jager
        ).summary()

        self.assertIn(
            "experiments",
            summary,
        )


if __name__ == "__main__":

    unittest.main()
