from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import time
import uuid


@dataclass(frozen=True)
class EvidenceEvent:

    event_id: str
    event_type: str
    experiment_id: str
    timestamp: float
    payload: Dict[str, Any] = field(
        default_factory=dict
    )
    source: str = "jager"
    parent_event_id: Optional[str] = None

    @classmethod
    def create(
        cls,
        event_type: str,
        experiment_id: str,
        payload: Optional[
            Dict[str, Any]
        ] = None,
        source: str = "jager",
        parent_event_id: Optional[str] = None,
    ):

        return cls(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            experiment_id=experiment_id,
            timestamp=time.time(),
            payload=dict(payload or {}),
            source=source,
            parent_event_id=parent_event_id,
        )

    def to_dict(self):

        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "experiment_id":
                self.experiment_id,
            "timestamp": self.timestamp,
            "payload":
                dict(self.payload),
            "source": self.source,
            "parent_event_id":
                self.parent_event_id,
        }
