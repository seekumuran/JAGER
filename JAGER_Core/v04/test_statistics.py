import unittest

from .statistics import (
    mean,
    variance,
    standard_deviation,
    rate,
)


class TestStatistics(unittest.TestCase):

    def test_mean(self):
        self.assertEqual(
            mean([1, 2, 3]),
            2,
        )

    def test_empty_mean(self):
        self.assertEqual(
            mean([]),
            0.0,
        )

    def test_rate(self):
        self.assertEqual(
            rate(5, 10),
            0.5,
        )

    def test_zero_rate(self):
        self.assertEqual(
            rate(0, 0),
            0.0,
        )

    def test_variance(self):
        self.assertAlmostEqual(
            variance([1, 2, 3]),
            1.0,
        )

    def test_standard_deviation(self):
        self.assertAlmostEqual(
            standard_deviation([1, 2, 3]),
            1.0,
        )


if __name__ == "__main__":
    unittest.main()
