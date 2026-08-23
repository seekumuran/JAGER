from typing import Any, Dict

from ..api.jager import Jager

from .system_health import (
    SystemHealth,
)

from .integration_status import (
    IntegrationStatus,
)


class SystemReport:

    def __init__(
        self,
        jager: Jager,
    ):

        self.jager = jager

    def generate(self) -> Dict[
        str,
        Any,
    ]:

        health = SystemHealth(
            self.jager
        ).check()

        status = IntegrationStatus(
            self.jager
        ).snapshot()

        return {
            "health": health,
            "status": status,
            "targets":
                self.jager.targets(),
        }

    def healthy(self):

        return (
            self.generate()
            ["health"]
            ["healthy"]
        )
