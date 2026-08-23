import os
from typing import Any, Dict, Optional


class EnvironmentConfig:

    PREFIX = "JAGER_"

    def __init__(
        self,
        environ: Optional[
            Dict[str, str]
        ] = None,
    ):

        self.environ = (
            environ
            if environ is not None
            else dict(os.environ)
        )

    def get(
        self,
        key: str,
        default: Optional[str] = None,
    ):

        return self.environ.get(
            f"{self.PREFIX}{key.upper()}",
            default,
        )

    def get_bool(
        self,
        key: str,
        default: bool = False,
    ):

        value = self.get(key)

        if value is None:
            return default

        return value.strip().lower() in {
            "1",
            "true",
            "yes",
            "on",
        }

    def get_int(
        self,
        key: str,
        default: int = 0,
    ):

        value = self.get(key)

        if value is None:
            return default

        return int(value)

    def get_float(
        self,
        key: str,
        default: float = 0.0,
    ):

        value = self.get(key)

        if value is None:
            return default

        return float(value)

    def as_dict(self):

        result = {}

        prefix = self.PREFIX

        for key, value in self.environ.items():

            if key.startswith(prefix):

                clean_key = key[
                    len(prefix):
                ].lower()

                result[clean_key] = value

        return result
