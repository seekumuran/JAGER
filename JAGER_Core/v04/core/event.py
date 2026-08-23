from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional
import uuid


@dataclass
class JagerEvent:

    event_type: str

    source: str = "runtime"

    payload: Any = None

    event_id: str = field(
        default_factory=lambda: str(
            uuid.uuid4()
        )
    )

    timestamp: str = field(
        default_factory=lambda:
            datetime.now(
                timezone.utc
            ).isoformat()
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self):

        return {
            "event_id":
                self.event_id,
            "event_type":
                self.event_type,
            "source":
                self.source,
            "timestamp":
                self.timestamp,
            "payload":
                self.payload,
            "metadata":
                dict(self.metadata),
        }
