from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class HealthStatus:

    healthy: bool

    status: str

    checks: Dict[str, Any]

    def to_dict(self):

        return {
            "healthy": self.healthy,
            "status": self.status,
            "checks": dict(self.checks),
        }


class HealthChecker:

    def __init__(self, jager):

        self.jager = jager

    def check(self) -> HealthStatus:

        checks = {
            "engine":
                self._engine_check(),
            "configuration":
                self._configuration_check(),
            "runtime":
                self._runtime_check(),
        }

        healthy = all(
            check["healthy"]
            for check in checks.values()
        )

        return HealthStatus(
            healthy=healthy,
            status=(
                "healthy"
                if healthy
                else "unhealthy"
            ),
            checks=checks,
        )

    def _engine_check(self):

        return {
            "healthy": True,
            "started":
                self.jager.engine.started,
        }

    def _configuration_check(self):

        try:

            self.jager.engine.config.validate()

            return {
                "healthy": True,
            }

        except Exception as exc:

            return {
                "healthy": False,
                "error": str(exc),
            }

    def _runtime_check(self):

        try:

            snapshot = (
                self.jager.snapshot()
            )

            return {
                "healthy": True,
                "available": snapshot
                is not None,
            }

        except Exception as exc:

            return {
                "healthy": False,
                "error": str(exc),
            }
