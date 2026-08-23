from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from .errors import ConfigurationError


@dataclass
class JagerConfig:

    name: str = "jager"

    version: str = "0.4"

    environment: str = "development"

    debug: bool = False

    data_directory: str = "data"

    max_iterations: int = 10

    max_failures: int = 3

    max_actions: int = 100

    max_risk: float = 1.0

    target_score: Optional[float] = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    def validate(self):

        if not self.name.strip():

            raise ConfigurationError(
                "name cannot be empty"
            )

        if self.max_iterations <= 0:

            raise ConfigurationError(
                "max_iterations must be > 0"
            )

        if self.max_failures < 0:

            raise ConfigurationError(
                "max_failures cannot be negative"
            )

        if self.max_actions <= 0:

            raise ConfigurationError(
                "max_actions must be > 0"
            )

        if not 0.0 <= self.max_risk <= 1.0:

            raise ConfigurationError(
                "max_risk must be between 0 and 1"
            )

        if (
            self.target_score is not None
            and not 0.0 <= self.target_score <= 1.0
        ):

            raise ConfigurationError(
                "target_score must be between 0 and 1"
            )

        return True

    def to_dict(self):

        return {
            "name": self.name,
            "version": self.version,
            "environment": self.environment,
            "debug": self.debug,
            "data_directory":
                self.data_directory,
            "max_iterations":
                self.max_iterations,
            "max_failures":
                self.max_failures,
            "max_actions":
                self.max_actions,
            "max_risk":
                self.max_risk,
            "target_score":
                self.target_score,
            "metadata":
                dict(self.metadata),
        }

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
    ):

        config = cls(
            name=data.get(
                "name",
                "jager",
            ),
            version=data.get(
                "version",
                "0.4",
            ),
            environment=data.get(
                "environment",
                "development",
            ),
            debug=data.get(
                "debug",
                False,
            ),
            data_directory=data.get(
                "data_directory",
                "data",
            ),
            max_iterations=data.get(
                "max_iterations",
                10,
            ),
            max_failures=data.get(
                "max_failures",
                3,
            ),
            max_actions=data.get(
                "max_actions",
                100,
            ),
            max_risk=data.get(
                "max_risk",
                1.0,
            ),
            target_score=data.get(
                "target_score"
            ),
            metadata=dict(
                data.get(
                    "metadata",
                    {},
                )
            ),
        )

        config.validate()

        return config
