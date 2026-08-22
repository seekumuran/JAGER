import unittest

from .baseline import RandomBaseline


class FakeTarget:

    def observe(self, **inputs):
        return {
            "status": "NORMAL",
            "inputs": inputs,
        }


class TestRandomBaseline(unittest.TestCase):

    def test_budget(self):
        baseline = RandomBaseline(
            FakeTarget(),
            seed=42,
        )

        results = baseline.run(10)

        self.assertEqual(
            len(results),
            10,
        )

    def test_reproducibility(self):
        first = RandomBaseline(
            FakeTarget(),
            seed=42,
        ).run(5)

        second = RandomBaseline(
            FakeTarget(),
            seed=42,
        ).run(5)

        self.assertEqual(
            first,
            second,
        )


if __name__ == "__main__":
    unittest.main()
