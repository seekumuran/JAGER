import time

from .protocol_state import (
    ProtocolState,
    ProtocolStateMachine,
)


class ProtocolExecutor:

    def __init__(
        self,
        hunter,
        protocol,
    ):
        self.hunter = hunter
        self.protocol = protocol

        self.state_machine = (
            ProtocolStateMachine()
        )

        self.events = []

    def _event(
        self,
        step,
        status,
        details=None,
    ):
        event = {
            "step": step,
            "status": status,
            "timestamp": time.time(),
            "details": details or {},
        }

        self.events.append(event)

        return event

    def initialize(self):
        self.state_machine.transition(
            ProtocolState.INITIALIZED
        )

        return self._event(
            "INITIALIZE",
            "COMPLETED",
        )

    def baseline(self):
        self.state_machine.transition(
            ProtocolState.BASELINE
        )

        result = (
            self.hunter.run_experiment()
        )

        return self._event(
            "BASELINE",
            "COMPLETED",
            {
                "experiment_id":
                    result["experiment_id"],
            },
        )

    def explore(self):
        self.state_machine.transition(
            ProtocolState.EXPLORING
        )

        result = []

        remaining = max(
            0,
            self.hunter.budget
            - len(
                self.hunter.experiments
            ),
        )

        for _ in range(remaining):
            result.append(
                self.hunter.run_experiment()
            )

        return self._event(
            "EXPLORE",
            "COMPLETED",
            {
                "experiments":
                    len(result),
            },
        )

    def refine(self):
        self.state_machine.transition(
            ProtocolState.REFINING
        )

        return self._event(
            "REFINE",
            "COMPLETED",
            {
                "discoveries":
                    len(
                        self.hunter.failed_discoveries
                    ),
            },
        )

    def verify(self):
        self.state_machine.transition(
            ProtocolState.VERIFYING
        )

        discoveries = (
            self.hunter.failed_discoveries
        )

        verified = []

        for discovery in discoveries:
            verified.append(
                {
                    "experiment_id":
                        discovery[
                            "experiment_id"
                        ],
                    "status":
                        discovery.get(
                            "status",
                            "FAILED",
                        ),
                }
            )

        return self._event(
            "VERIFY",
            "COMPLETED",
            {
                "candidates":
                    len(discoveries),
                "verified":
                    len(verified),
            },
        )

    def finalize(self):
        self.state_machine.transition(
            ProtocolState.FINALIZED
        )

        return self._event(
            "FINALIZE",
            "COMPLETED",
            {
                "experiments":
                    len(
                        self.hunter.experiments
                    ),
                "discoveries":
                    len(
                        self.hunter.failed_discoveries
                    ),
            },
        )

    def run(self):
        try:
            self.protocol.validate()

            self.initialize()
            self.baseline()
            self.explore()

            if self.hunter.failed_discoveries:
                self.refine()
                self.verify()

            self.finalize()

            return {
                "state":
                    self.state_machine.current(),
                "history":
                    self.state_machine.history,
                "events":
                    self.events,
            }

        except Exception as exc:
            try:
                self.state_machine.transition(
                    ProtocolState.FAILED
                )
            except ValueError:
                pass

            self._event(
                "PROTOCOL",
                "FAILED",
                {
                    "error": str(exc)
                },
            )

            raise
