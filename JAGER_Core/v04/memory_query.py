from .experience_similarity import (
    ExperienceSimilarity,
)


class MemoryQuery:

    def __init__(self, memory):
        self.memory = memory
        self.similarity = ExperienceSimilarity()

    def nearest(
        self,
        inputs,
        limit=5,
    ):
        ranked = []

        for experience in self.memory.items:
            score = self.similarity.similarity(
                inputs,
                experience.action.parameters,
            )

            ranked.append(
                (
                    score,
                    experience,
                )
            )

        ranked.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return ranked[:limit]

    def failures_near(
        self,
        inputs,
        limit=5,
    ):
        results = []

        for score, experience in self.nearest(
            inputs,
            limit=limit * 3,
        ):
            if experience.observation.status == "FAILED":
                results.append(
                    (
                        score,
                        experience,
                    )
                )

            if len(results) >= limit:
                break

        return results
