from typing import Dict

from ..api.jager import Jager

from .health_check import (
    HealthChecker,
)


class SystemHealth:

    def __init__(
        self,
        jager: Jager,
    ):

        self.jager = jager

        self.checker = (
            HealthChecker()
        )

    def check(self):

        components: Dict[
            str,
            bool,
        ] = {
            "registry":
                self.jager.registry.size()
                >= 0,

            "configuration":
                self.jager.config is not None,

            "runtime":
                self.jager.runtime is not None,

            "state":
                self.jager.runtime.state
                is not None,
        }

        results = (
            self.checker.check_all(
                components
            )
        )

        return {
            "healthy":
                self.checker.healthy(
                    components
                ),
            "components": [
                {
                    "component":
                        result.component,
                    "healthy":
                        result.healthy,
                    "message":
                        result.message,
                }
                for result in results
            ],
        }
