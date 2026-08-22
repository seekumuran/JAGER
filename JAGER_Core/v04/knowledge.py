from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class Knowledge:
    pattern: str
    evidence: Dict[str, Any]
    confidence: float
    observations: int = 0

    def update(
        self,
        evidence,
        confidence,
    ):
        self.evidence = evidence
        self.confidence = confidence
        self.observations += 1

    def to_dict(self):
        return asdict(self)


class KnowledgeBase:

    def __init__(self):
        self.entries = {}

    def add(
        self,
        key,
        pattern,
        evidence,
        confidence,
    ):
        if key not in self.entries:
            self.entries[key] = Knowledge(
                pattern=pattern,
                evidence=evidence,
                confidence=confidence,
                observations=1,
            )
        else:
            self.entries[key].update(
                evidence,
                confidence,
            )

        return self.entries[key]

    def get(self, key):
        return self.entries.get(key)

    def all(self):
        return list(
            self.entries.values()
        )

    def __len__(self):
        return len(self.entries)
