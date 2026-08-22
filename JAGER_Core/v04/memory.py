from typing import List, Optional

from .models import Experience


class ExperienceMemory:
    def __init__(self, capacity: int = 10000):
        self.capacity = capacity
        self.items: List[Experience] = []

    def store(self, experience: Experience):
        self.items.append(experience)

        if len(self.items) > self.capacity:
            self.items.pop(0)

    def retrieve(
        self,
        limit: int = 10,
    ) -> List[Experience]:
        return sorted(
            self.items,
            key=lambda x: (
                x.useful,
                x.reward,
                x.novelty,
            ),
            reverse=True,
        )[:limit]

    def failures(self):
        return [
            x
            for x in self.items
            if x.observation.status == "FAILED"
        ]

    def __len__(self):
        return len(self.items)
