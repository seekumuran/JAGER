from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional


@dataclass
class Experience:
    experiment_id: str
    inputs: Dict[str, Any]
    telemetry: Dict[str, Any]
    status: str
    discovery: bool
    reward: float
    usefulness: float

    def to_dict(self):
        return asdict(self)


class ExperienceStore:
    def __init__(self):
        self.items: List[Experience] = []

    def add(self, experience: Experience):
        self.items.append(experience)

    def recent(self, limit: int = 25) -> List[Experience]:
        return self.items[-limit:]

    def best(self) -> Optional[Experience]:
        if not self.items:
            return None

        return max(
            self.items,
            key=lambda item: item.usefulness,
        )

    def discoveries(self) -> List[Experience]:
        return [
            item
            for item in self.items
            if item.discovery
        ]

    def __len__(self):
        return len(self.items)
