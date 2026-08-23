import json
from pathlib import Path
from typing import List, Optional

from .checkpoint import (
    RuntimeCheckpoint,
)


class CheckpointStore:

    def __init__(
        self,
        directory: str = (
            "data/checkpoints"
        ),
    ):

        self.directory = Path(
            directory
        )

        self.directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def _path(
        self,
        checkpoint_id: str,
    ):

        return (
            self.directory
            / f"{checkpoint_id}.json"
        )

    def save(
        self,
        checkpoint: RuntimeCheckpoint,
    ):

        path = self._path(
            checkpoint.checkpoint_id
        )

        temporary = path.with_suffix(
            ".tmp"
        )

        with temporary.open(
            "w",
            encoding="utf-8",
        ) as handle:

            json.dump(
                checkpoint.to_dict(),
                handle,
                indent=2,
            )

        temporary.replace(path)

    def load(
        self,
        checkpoint_id: str,
    ) -> Optional[
        RuntimeCheckpoint
    ]:

        path = self._path(
            checkpoint_id
        )

        if not path.exists():

            return None

        with path.open(
            "r",
            encoding="utf-8",
        ) as handle:

            data = json.load(handle)

        return RuntimeCheckpoint.from_dict(
            data
        )

    def exists(
        self,
        checkpoint_id: str,
    ) -> bool:

        return self._path(
            checkpoint_id
        ).exists()

    def delete(
        self,
        checkpoint_id: str,
    ):

        path = self._path(
            checkpoint_id
        )

        if path.exists():

            path.unlink()

    def list(
        self,
    ) -> List[
        RuntimeCheckpoint
    ]:

        checkpoints = []

        for path in sorted(
            self.directory.glob(
                "*.json"
            )
        ):

            with path.open(
                "r",
                encoding="utf-8",
            ) as handle:

                data = json.load(handle)

            checkpoints.append(
                RuntimeCheckpoint.from_dict(
                    data
                )
            )

        return checkpoints
