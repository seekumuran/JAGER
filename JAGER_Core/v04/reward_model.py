class RewardModel:

    STATUS_REWARDS = {
        "NORMAL": 0.1,
        "DEGRADED": 2.0,
        "FAILED": 10.0,
    }

    def calculate(
        self,
        status,
        novelty,
        confirmed=False,
    ):
        reward = self.STATUS_REWARDS.get(
            status,
            0.0,
        )

        reward += novelty * 2.0

        if confirmed:
            reward += 5.0

        return reward
