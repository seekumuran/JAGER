from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional
import uuid


@dataclass
class RuntimeSession:

    session_id: str = field(
        default_factory=lambda: str(
            uuid.uuid4()
        )
    )

    experiment_id: Optional[str] = None

    status: str = "created"

    created_at: str = field(
        default_factory=lambda:
            datetime.now(
                timezone.utc
            ).isoformat()
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    def start(
        self,
        experiment_id: str,
    ):

        if self.status != "created":

            raise RuntimeError(
                f"cannot start session "
                f"from {self.status}"
            )

        self.experiment_id = (
            experiment_id
        )

        self.status = "active"

    def pause(self):

        if self.status != "active":

            raise RuntimeError(
                "session is not active"
            )

        self.status = "paused"

    def resume(self):

        if self.status != "paused":

            raise RuntimeError(
                "session is not paused"
            )

        self.status = "active"

    def close(self):

        if self.status not in {
            "active",
            "paused",
        }:

            raise RuntimeError(
                f"cannot close session "
                f"from {self.status}"
            )

        self.status = "closed"

    def is_active(self):

        return self.status == "active"

    def is_closed(self):

        return self.status == "closed"

    def snapshot(self):

        return {
            "session_id":
                self.session_id,
            "experiment_id":
                self.experiment_id,
            "status":
                self.status,
            "created_at":
                self.created_at,
            "metadata":
                dict(self.metadata),
        }
