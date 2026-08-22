from typing import List, Optional

from .experience import Experience


class ExperienceMemory:
    """Simple persistent experience store for v0.2."""

    def __init__(self):
        self.experiences: List[Experience] = []

    def add(self, experience: Experience):
        self.experiences.append(experience)

    def retrieve(self) -> Optional[Experience]:
        if not self.experiences:
            return None

        # Prefer the most useful known experience.
        return max(
            self.experiences,
            key=lambda experience: experience.usefulness
        )

    def __len__(self):
        return len(self.experiences)
