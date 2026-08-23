import json
from pathlib import Path
from typing import Any, Dict, Optional

from ..core.config import JagerConfig


class ConfigLoader:

    def __init__(
        self,
        default_path: Optional[
            str
        ] = None,
    ):

        self.default_path = (
            Path(default_path)
            if default_path
            else Path(__file__).parent
            / "default.json"
        )

    def load_file(
        self,
        path: str,
    ) -> JagerConfig:

        file_path = Path(path)

        if not file_path.exists():

            raise FileNotFoundError(
                file_path
            )

        with file_path.open(
            "r",
            encoding="utf-8",
        ) as handle:

            data = json.load(handle)

        return JagerConfig.from_dict(
            data
        )

    def load_default(
        self,
    ) -> JagerConfig:

        return self.load_file(
            str(self.default_path)
        )

    def load(
        self,
        path: Optional[str] = None,
        overrides: Optional[
            Dict[str, Any]
        ] = None,
    ) -> JagerConfig:

        config = (
            self.load_file(path)
            if path
            else self.load_default()
        )

        if overrides:

            data = config.to_dict()
            data.update(overrides)

            config = (
                JagerConfig.from_dict(
                    data
                )
            )

        return config
