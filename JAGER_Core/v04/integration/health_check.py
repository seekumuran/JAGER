from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class HealthCheckResult:

    component: str
    healthy: bool
    message: str


class HealthChecker:

    def check_component(
        self,
        component: str,
        available: bool,
    ) -> HealthCheckResult:

        if available:

            return HealthCheckResult(
                component=component,
                healthy=True,
                message="available",
            )

        return HealthCheckResult(
            component=component,
            healthy=False,
            message="unavailable",
        )

    def check_all(
        self,
        components: Dict[str, bool],
    ) -> List[
        HealthCheckResult
    ]:

        return [
            self.check_component(
                component=name,
                available=available,
            )
            for name, available
            in components.items()
        ]

    def healthy(
        self,
        components: Dict[str, bool],
    ) -> bool:

        return all(
            components.values()
        )
