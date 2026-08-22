import math
import random


class AdaptiveSearch:

    def __init__(
        self,
        seed=42,
        exploration=1.0,
    ):
        self.random = random.Random(seed)
        self.exploration = exploration

        self.actions = []
        self.action_scores = {}

    def select(
        self,
        candidates,
    ):

        if not candidates:
            raise ValueError(
                "No candidates available."
            )

        # Always explore unseen actions first.
        unseen = [
            candidate
            for candidate in candidates
            if self._key(candidate)
            not in self.action_scores
        ]

        if unseen:
            return self.random.choice(
                unseen
            )

        total = max(
            1,
            len(self.actions)
        )

        scored = []

        for candidate in candidates:

            key = self._key(
                candidate
            )

            count, reward = (
                self.action_scores[key]
            )

            average_reward = (
                reward / count
            )

            confidence_bonus = (
                self.exploration
                * math.sqrt(
                    math.log(total)
                    / count
                )
            )

            score = (
                average_reward
                + confidence_bonus
            )

            scored.append(
                (
                    score,
                    candidate,
                )
            )

        scored.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return scored[0][1]

    def update(
        self,
        action,
        reward,
    ):

        key = self._key(action)

        if key not in self.action_scores:

            self.action_scores[key] = (
                0,
                0.0,
            )

        count, total_reward = (
            self.action_scores[key]
        )

        self.action_scores[key] = (
            count + 1,
            total_reward + reward,
        )

        self.actions.append(
            action
        )

    @staticmethod
    def _key(action):

        return repr(
            sorted(
                action.items()
            )
        )

    def statistics(self):

        result = {}

        for key, (
            count,
            reward,
        ) in self.action_scores.items():

            result[key] = {
                "count": count,
                "total_reward": reward,
                "average_reward": (
                    reward / count
                    if count
                    else 0.0
                ),
            }

        return result
