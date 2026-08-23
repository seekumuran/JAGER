import json
from pathlib import Path
from typing import Any, Dict, Optional

from .config import JagerConfig


class ConfigLoader:

    def load_dict(
        self,
        values: Optional[
            Dict[str, Any]
        ] = None,
    ):

        config = JagerConfig(
            **dict(values or {})
        )

        return config.validate()

    def load_file(
        self,
        path: str,
    ):

        config_path = Path(path)

        if not config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: "
                f"{path}"
            )

        with config_path.open(
            "r",
            encoding="utf-8",
        ) as handle:

            values = json.load(handle)

        if not isinstance(values, dict):
            raise ValueError(
                "Configuration root must be an object"
            )

        return self.load_dict(values)

    def save_file(
        self,
        config: JagerConfig,
        path: str,
    ):

        config.validate()

        config_path = Path(path)

        config_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with config_path.open(
            "w",
            encoding="utf-8",
        ) as handle:

            json.dump(
                config.to_dict(),
                handle,
                indent=2,
            )

        return config_path
