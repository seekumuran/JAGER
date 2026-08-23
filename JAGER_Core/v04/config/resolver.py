from typing import Any, Dict, Optional

from ..core.config import JagerConfig

from .environment import (
    EnvironmentConfig,
)


class ConfigResolver:

    def __init__(
        self,
        environment: Optional[
            EnvironmentConfig
        ] = None,
    ):

        self.environment = (
            environment
            or EnvironmentConfig()
        )

    def resolve(
        self,
        config: Optional[
            JagerConfig
        ] = None,
        overrides: Optional[
            Dict[str, Any]
        ] = None,
    ) -> JagerConfig:

        base = (
            config.to_dict()
            if config
            else JagerConfig().to_dict()
        )

        environment = (
            self.environment.as_dict()
        )

        base.update(
            self._convert(
                environment
            )
        )

        if overrides:
            base.update(overrides)

        return JagerConfig.from_dict(
            base
        )

    def _convert(
        self,
        values: Dict[str, Any],
    ):

        converted = {}

        integer_keys = {
            "max_iterations",
            "max_failures",
            "max_actions",
        }

        float_keys = {
            "max_risk",
            "target_score",
        }

        bool_keys = {
            "debug",
        }

        for key, value in values.items():

            if key in integer_keys:

                converted[key] = int(value)

            elif key in float_keys:

                if value.lower() == "none":

                    converted[key] = None

                else:

                    converted[key] = float(
                        value
                    )

            elif key in bool_keys:

                converted[key] = (
                    value.lower()
                    in {
                        "1",
                        "true",
                        "yes",
                        "on",
                    }
                )

            else:

                converted[key] = value

        return converted
