import unittest

from .end_to_end import (
    build_mock_runtime,
)

from .system_report import (
    SystemReport,
)


class TestEndToEnd(
    unittest.TestCase
):

    def test_system_report(self):

        jager = build_mock_runtime()

        report = SystemReport(
            jager
        ).generate()

        self.assertTrue(
            report["health"]["healthy"]
        )

        self.assertIn(
            "mock",
            report["targets"],
        )

    def test_report_health(self):

        jager = build_mock_runtime()

        report = SystemReport(
            jager
        )

        self.assertTrue(
            report.healthy()
        )


if __name__ == "__main__":
    unittest.main()
