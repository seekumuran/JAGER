from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import time
import uuid


@dataclass
class DiscoveryRecord:

    discovery_id: str
    experiment_id: str
    target: str

    category: str
    severity: str

    novelty: float
    confidence: float

    evidence_event_ids: List[str] = field(
        default_factory=list
    )

    description: str = ""

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    created_at: float = field(
        default_factory=time.time
    )

    @classmethod
    def create(
        cls,
        experiment_id: str,
        target: str,
        category: str,
        severity: str,
        novelty: float,
        confidence: float,
        evidence_event_ids=None,
        description: str = "",
        metadata=None,
    ):

        return cls(
            discovery_id=str(uuid.uuid4()),
            experiment_id=experiment_id,
            target=target,
            category=category,
            severity=severity,
            novelty=float(novelty),
            confidence=float(confidence),
            evidence_event_ids=list(
                evidence_event_ids or []
            ),
            description=description,
            metadata=dict(metadata or {}),
        )

    def to_dict(self):

        return {
            "discovery_id":
                self.discovery_id,
            "experiment_id":
                self.experiment_id,
            "target":
                self.target,
            "category":
                self.category,
            "severity":
                self.severity,
            "novelty":
                self.novelty,
            "confidence":
                self.confidence,
            "evidence_event_ids":
                list(
                    self.evidence_event_ids
                ),
            "description":
                self.description,
            "metadata":
                dict(self.metadata),
            "created_at":
                self.created_at,
        }
