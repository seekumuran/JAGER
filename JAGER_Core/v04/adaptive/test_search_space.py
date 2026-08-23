import unittest

from .search_space import (
    SearchSpace,
)


class TestSearchSpace(
    unittest.TestCase
):

    def test_float_sampling(self):

        space = SearchSpace(
            seed=42
        )

        space.add_float(
            "cpu_load",
            0,
            100,
        )

        value = space.sample()[
            "cpu_load"
        ]

        self.assertGreaterEqual(
            value,
            0,
        )

        self.assertLessEqual(
            value,
            100,
        )

    def test_integer_sampling(self):

        space = SearchSpace(
            seed=42
        )

        space.add_int(
            "processes",
            1,
            10,
        )

        value = space.sample()[
            "processes"
        ]

        self.assertIsInstance(
            value,
            int,
        )

        self.assertGreaterEqual(
            value,
            1,
        )

        self.assertLessEqual(
            value,
            10,
        )

    def test_choice_sampling(self):

        space = SearchSpace(
            seed=42
        )

        space.add_choice(
            "mode",
            [
                "normal",
                "stress",
            ],
        )

        value = space.sample()[
            "mode"
        ]

        self.assertIn(
            value,
            [
                "normal",
                "stress",
            ],
        )

    def test_reproducibility(self):

        first = SearchSpace(
            seed=123
        )

        second = SearchSpace(
            seed=123
        )

        for space in (
            first,
            second,
        ):
            space.add_float(
                "cpu",
                0,
                100,
            )

            space.add_int(
                "processes",
                1,
                100,
            )

        self.assertEqual(
            first.sample_many(10),
            second.sample_many(10),
        )

    def test_invalid_range(self):

        space = SearchSpace()

        with self.assertRaises(
            ValueError
        ):
            space.add_float(
                "cpu",
                100,
                0,
            )

    def test_sample_many(self):

        space = SearchSpace()

        space.add_int(
            "x",
            0,
            10,
        )

        values = space.sample_many(
            20
        )

        self.assertEqual(
            len(values),
            20,
        )


if __name__ == "__main__":
    unittest.main()
