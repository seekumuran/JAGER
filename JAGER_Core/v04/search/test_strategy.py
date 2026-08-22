import unittest

from .strategy import AdaptiveSearch


class TestAdaptiveSearch(
    unittest.TestCase
):

    def test_unseen_action_is_selected(self):

        search = AdaptiveSearch(
            seed=42
        )

        candidates = [
            {
                "type": "a"
            },
            {
                "type": "b"
            },
        ]

        selected = search.select(
            candidates
        )

        self.assertIn(
            selected,
            candidates,
        )

    def test_update_records_result(self):

        search = AdaptiveSearch(
            seed=42
        )

        action = {
            "type": "a"
        }

        search.update(
            action,
            1.0,
        )

        stats = search.statistics()

        self.assertEqual(
            len(stats),
            1,
        )

    def test_average_reward(self):

        search = AdaptiveSearch(
            seed=42
        )

        action = {
            "type": "a"
        }

        search.update(
            action,
            1.0,
        )

        search.update(
            action,
            3.0,
        )

        stats = search.statistics()

        values = list(
            stats.values()
        )

        self.assertEqual(
            values[0][
                "average_reward"
            ],
            2.0,
        )

    def test_empty_candidates(self):

        search = AdaptiveSearch()

        with self.assertRaises(
            ValueError
        ):
            search.select([])


if __name__ == "__main__":
    unittest.main()
