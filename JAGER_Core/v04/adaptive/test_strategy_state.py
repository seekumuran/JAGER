import unittest

from .strategy_state import (
    StrategyState,
)


class TestStrategyState(
    unittest.TestCase
):

    def test_state_tracking(self):

        state = StrategyState()

        state.record_iteration(
            "blackbox"
        )

        state.record_exploration()
        state.record_exploitation()
        state.record_discovery()

        snapshot = state.snapshot()

        self.assertEqual(
            snapshot["iterations"],
            1,
        )

        self.assertEqual(
            snapshot["explorations"],
            1,
        )

        self.assertEqual(
            snapshot["exploitations"],
            1,
        )

        self.assertEqual(
            snapshot["discoveries"],
            1,
        )

        self.assertEqual(
            snapshot[
                "target_iterations"
            ]["blackbox"],
            1,
        )


if __name__ == "__main__":
    unittest.main()
