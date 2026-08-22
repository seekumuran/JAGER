from enum import Enum


class ProtocolState(str, Enum):
    CREATED = "CREATED"
    INITIALIZED = "INITIALIZED"
    BASELINE = "BASELINE"
    EXPLORING = "EXPLORING"
    REFINING = "REFINING"
    VERIFYING = "VERIFYING"
    FINALIZED = "FINALIZED"
    FAILED = "FAILED"


class ProtocolStateMachine:

    TRANSITIONS = {
        ProtocolState.CREATED: {
            ProtocolState.INITIALIZED,
            ProtocolState.FAILED,
        },
        ProtocolState.INITIALIZED: {
            ProtocolState.BASELINE,
            ProtocolState.FAILED,
        },
        ProtocolState.BASELINE: {
            ProtocolState.EXPLORING,
            ProtocolState.FAILED,
        },
        ProtocolState.EXPLORING: {
            ProtocolState.REFINING,
            ProtocolState.FINALIZED,
            ProtocolState.FAILED,
        },
        ProtocolState.REFINING: {
            ProtocolState.EXPLORING,
            ProtocolState.VERIFYING,
            ProtocolState.FAILED,
        },
        ProtocolState.VERIFYING: {
            ProtocolState.EXPLORING,
            ProtocolState.FINALIZED,
            ProtocolState.FAILED,
        },
        ProtocolState.FINALIZED: set(),
        ProtocolState.FAILED: set(),
    }

    def __init__(self):
        self.state = ProtocolState.CREATED
        self.history = [
            self.state.value
        ]

    def transition(self, new_state):
        if not isinstance(
            new_state,
            ProtocolState,
        ):
            new_state = ProtocolState(
                new_state
            )

        allowed = self.TRANSITIONS[
            self.state
        ]

        if new_state not in allowed:
            raise ValueError(
                f"Invalid protocol transition: "
                f"{self.state.value} -> "
                f"{new_state.value}"
            )

        self.state = new_state
        self.history.append(
            new_state.value
        )

        return self.state

    def current(self):
        return self.state.value

    def completed(self):
        return self.state in {
            ProtocolState.FINALIZED,
            ProtocolState.FAILED,
        }
