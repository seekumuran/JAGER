from typing import Any, Dict, Optional

from .checkpoint import (
    RuntimeCheckpoint,
)

from .checkpoint_store import (
    CheckpointStore,
)


class CheckpointManager:

    def __init__(
        self,
        store: CheckpointStore,
    ):

        self.store = store

    def create(
        self,
        checkpoint_id: str,
        iteration: int,
        status: str,
        state: Dict[str, Any],
        experiment_id: Optional[str] = None,
        metadata: Optional[
            Dict[str, Any]
        ] = None,
    ) -> RuntimeCheckpoint:

        checkpoint = RuntimeCheckpoint(
            checkpoint_id=checkpoint_id,
            iteration=iteration,
            status=status,
            experiment_id=experiment_id,
            state=dict(state),
            metadata=dict(
                metadata or {}
            ),
        )

        self.store.save(
            checkpoint
        )

        return checkpoint

    def restore(
        self,
        checkpoint_id: str,
    ) -> Optional[
        RuntimeCheckpoint
    ]:

        return self.store.load(
            checkpoint_id
        )

    def latest(self):

        checkpoints = self.store.list()

        if not checkpoints:

            return None

        return max(
            checkpoints,
            key=lambda item:
                item.iteration,
        )

    def remove(
        self,
        checkpoint_id: str,
    ):

        self.store.delete(
            checkpoint_id
        )
