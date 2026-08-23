from typing import Any, Dict


class Diagnostics:

    def __init__(self, jager):

        self.jager = jager

    def snapshot(self) -> Dict[str, Any]:

        snapshot = self.jager.snapshot()

        return {
            "version":
                self.jager.engine.config.version,
            "environment":
                self.jager.engine.config.environment,
            "started":
                self.jager.engine.started,
            "runtime":
                snapshot["runtime"],
        }

    def summary(self):

        snapshot = self.snapshot()

        runtime = snapshot["runtime"]

        experiments = runtime[
            "experiments"
        ]

        return {
            "version":
                snapshot["version"],
            "environment":
                snapshot["environment"],
            "started":
                snapshot["started"],
            "experiments":
                len(experiments),
        }
