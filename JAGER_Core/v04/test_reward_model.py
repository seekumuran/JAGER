import unittest

from .reward_model import RewardModel


class TestRewardModel(unittest.TestCase):

    def test_failure_reward_higher(self):
        model = RewardModel()

        normal = model.calculate(
            "NORMAL",
            0.5,
        )

        failure = model.calculate(
            "FAILED",
            0.5,
        )

        self.assertGreater(
            failure,
            normal,
        )

    def test_confirmation_increases_reward(self):
        model = RewardModel()

        without = model.calculate(
            "FAILED",
            1.0,
            confirmed=False,
        )

        with_confirmation = model.calculate(
            "FAILED",
            1.0,
            confirmed=True,
        )

        self.assertGreater(
            with_confirmation,
            without,
        )


if __name__ == "__main__":
    unittest.main()
