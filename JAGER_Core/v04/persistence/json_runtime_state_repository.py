import json
from pathlib import Path
from typing import Optional

from ..state.runtime_state import (
    RuntimeState,
)

from .runtime_state_repository import (
    RuntimeStateRepository,
)


class JsonRuntimeStateRepository(
    RuntimeStateRepository
):

    def __init__(self, path: str):

        self.path = Path(path)

    def save(
        self,
        state: RuntimeState,
    ):

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        temporary = self.path.with_suffix(
            self.path.suffix + ".tmp"
        )

        with temporary.open(
            "w",
            encoding="utf-8",
        ) as handle:

            json.dump(
                state.to_dict(),
                handle,
                indent=2,
            )

        temporary.replace(self.path)

    def load(
        self,
    ) -> Optional[RuntimeState]:

        if not self.path.exists():
            return None

        with self.path.open(
            "r",
            encoding="utf-8",
        ) as handle:

            data = json.load(handle)

        if not isinstance(data, dict):
            raise ValueError(
                "Runtime state must be "
                "stored as a JSON object"
            )

        return RuntimeState(
            started_at=data.get(
                "started_at"
            ),
            active_experiment_id=data.get(
                "active_experiment_id"
            ),
            iteration=data.get(
                "iteration",
                0,
            ),
            status=data.get(
                "status",
                "idle",
            ),
            experiments_completed=data.get(
                "experiments_completed",
                0,
            ),
            experiments_failed=data.get(
                "experiments_failed",
                0,
            ),
            discoveries_found=data.get(
                "discoveries_found",
                0,
            ),
            experiences_created=data.get(
                "experiences_created",
                0,
            ),
            metadata=dict(
                data.get("metadata", {})
            ),
            history=list(
                data.get("history", [])
            ),
        )

    def clear(self):

        if self.path.exists():
            self.path.unlink()
