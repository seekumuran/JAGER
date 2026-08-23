from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import time
import uuid


@dataclass
class ExperienceRecord:

    experience_id: str
    target: str
    hypothesis: str
    action: Dict[str, Any]
    outcome: Dict[str, Any]

    discovery: bool = False
    novelty: float = 0.0
    confidence: float = 0.0

    tags: List[str] = field(
        default_factory=list
    )

    created_at: float = field(
        default_factory=time.time
    )

    parent_experience_id: Optional[
        str
    ] = None

    @classmethod
    def create(
        cls,
        target: str,
        hypothesis: str,
        action: Dict[str, Any],
        outcome: Dict[str, Any],
        discovery: bool = False,
        novelty: float = 0.0,
        confidence: float = 0.0,
        tags: Optional[List[str]] = None,
        parent_experience_id=None,
    ):

        return cls(
            experience_id=str(
                uuid.uuid4()
            ),
            target=target,
            hypothesis=hypothesis,
            action=dict(action),
            outcome=dict(outcome),
            discovery=bool(discovery),
            novelty=float(novelty),
            confidence=float(confidence),
            tags=list(tags or []),
            parent_experience_id=(
                parent_experience_id
            ),
        )

    def to_dict(self):

        return {
            "experience_id":
                self.experience_id,
            "target":
                self.target,
            "hypothesis":
                self.hypothesis,
            "action":
                dict(self.action),
            "outcome":
                dict(self.outcome),
            "discovery":
                self.discovery,
            "novelty":
                self.novelty,
            "confidence":
                self.confidence,
            "tags":
                list(self.tags),
            "created_at":
                self.created_at,
            "parent_experience_id":
                self.parent_experience_id,
        }
