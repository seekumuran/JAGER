from typing import Dict, Any

from .action_schema import (
    ActionSchema,
)
from .base import (
    BaseTarget,
    TargetResult,
)


class TargetExecutor:

    def __init__(
        self,
        target: BaseTarget,
        schema=None,
    ):

        self.target = target

        self.schema = (
            schema
            or ActionSchema()
        )

    def execute(
        self,
        action: Dict[str, Any],
    ) -> TargetResult:

        validation = (
            self.schema.validate(
                self.target.name,
                action,
            )
        )

        if not validation.valid:

            return TargetResult(
                target=self.target.name,
                status="DENIED",
                telemetry={},
                metadata={
                    "reason":
                        validation.reason,
                    "validation":
                        validation.to_dict(),
                },
            )

        return self.target.observe(
            validation.normalized
        )
