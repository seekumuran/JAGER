from typing import Dict, Any, List


class MemoryGuidedPolicy:

    def __init__(self, memory):
        self.memory = memory

    def rank(
        self,
        candidates: List[Dict[str, Any]],
    ):

        history = self.memory.all()

        if not history:
            return candidates

        scores = []

        for candidate in candidates:

            score = 0.0

            candidate_type = (
                candidate.get("type")
            )

            for record in history:

                action = record.get(
                    "action",
                    {},
                )

                if action.get(
                    "type"
                ) != candidate_type:
                    continue

                reward = float(
                    record.get(
                        "reward",
                        0.0,
                    )
                )

                novelty = float(
                    record.get(
                        "novelty",
                        0.0,
                    )
                )

                score += (
                    reward * 0.7
                    + novelty * 0.3
                )

            scores.append(
                (
                    score,
                    candidate,
                )
            )

        scores.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            candidate
            for _, candidate
            in scores
        ]
