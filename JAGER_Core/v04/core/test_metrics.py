import tempfile
import unittest

from .metrics import MetricsRegistry
from .metrics_store import MetricsStore


class TestMetrics(
    unittest.TestCase
):

    def test_series(self):

        metrics = MetricsRegistry()

        metrics.record(
            "score",
            0.5,
            iteration=1,
        )

        metrics.record(
            "score",
            0.9,
            iteration=2,
        )

        series = metrics.get(
            "score"
        )

        self.assertEqual(
            series.count(),
            2,
        )

        self.assertAlmostEqual(
            series.mean(),
            0.7,
        )

        self.assertAlmostEqual(
            series.maximum(),
            0.9,
        )

        self.assertAlmostEqual(
            series.minimum(),
            0.5,
        )

    def test_store(self):

        with tempfile.TemporaryDirectory() as tmp:

            store = MetricsStore(
                f"{tmp}/metrics.json"
            )

            metrics = {
                "score": {
                    "mean": 0.8
                }
            }

            store.save(metrics)

            loaded = store.load()

            self.assertEqual(
                loaded["score"]["mean"],
                0.8,
            )


if __name__ == "__main__":

    unittest.main()
