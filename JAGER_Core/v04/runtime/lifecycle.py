from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass
class RuntimeLifecycle:

    status: str = "created"

    started_at: Optional[str] = None

    completed_at: Optional[str] = None

    reason: Optional[str] = None

    def start(self):

        if self.status not in {
            "created",
            "paused",
        }:

            raise RuntimeError(
                f"cannot start from "
                f"{self.status}"
            )

        self.status = "running"

        self.started_at = (
            datetime.now(
                timezone.utc
            ).isoformat()
        )

        self.reason = None

    def pause(
        self,
        reason: str = "paused",
    ):

        if self.status != "running":

            raise RuntimeError(
                "runtime is not running"
            )

        self.status = "paused"
        self.reason = reason

    def complete(
        self,
        reason: str = "completed",
    ):

        if self.status not in {
            "running",
            "paused",
        }:

            raise RuntimeError(
                f"cannot complete from "
                f"{self.status}"
            )

        self.status = "completed"

        self.completed_at = (
            datetime.now(
                timezone.utc
            ).isoformat()
        )

        self.reason = reason

    def fail(
        self,
        reason: str,
    ):

        self.status = "failed"

        self.completed_at = (
            datetime.now(
                timezone.utc
            ).isoformat()
        )

        self.reason = reason

    def cancel(
        self,
        reason: str = "cancelled",
    ):

        self.status = "cancelled"

        self.completed_at = (
            datetime.now(
                timezone.utc
            ).isoformat()
        )

        self.reason = reason

    def is_terminal(self):

        return self.status in {
            "completed",
            "failed",
            "cancelled",
        }

    def snapshot(self):

        return {
            "status": self.status,
            "started_at":
                self.started_at,
            "completed_at":
                self.completed_at,
            "reason":
                self.reason,
            "terminal":
                self.is_terminal(),
        }
