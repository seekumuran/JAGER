from typing import Any, Dict

from ..health import (
    HealthChecker,
    HealthStatus,
)

from ..diagnostics import (
    Diagnostics,
)


class HealthService:

    def __init__(self, jager):

        self.jager = jager

        self.health = HealthChecker(
            jager
        )

        self.diagnostics = Diagnostics(
            jager
        )

    def check(self) -> HealthStatus:

        return self.health.check()

    def status(self) -> Dict[str, Any]:

        return self.health.check().to_dict()

    def diagnostics_snapshot(
        self,
    ) -> Dict[str, Any]:

        return self.diagnostics.snapshot()

    def summary(self) -> Dict[str, Any]:

        return self.diagnostics.summary()
