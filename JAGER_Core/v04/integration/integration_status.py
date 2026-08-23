from typing import Any, Dict

from ..api.jager import Jager


class IntegrationStatus:

    def __init__(
        self,
        jager: Jager,
    ):

        self.jager = jager

    def snapshot(self) -> Dict[
        str,
        Any,
    ]:

        runtime = (
            self.jager.status()
        )

        return {
            "targets":
                self.jager.targets(),

            "target_count":
                len(
                    self.jager.targets()
                ),

            "runtime":
                runtime,

            "status":
                runtime.get(
                    "status",
                    "unknown",
                ),
        }
