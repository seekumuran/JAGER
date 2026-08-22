import unittest

from .protocol import (
    ExperimentProtocol,
)
from .protocol_state import (
    ProtocolState,
    ProtocolStateMachine,
)


class TestProtocol(unittest.TestCase):

    def test_default_protocol(self):
        protocol = ExperimentProtocol()

        self.assertTrue(
            protocol.validate()
        )

        self.assertEqual(
            protocol.step_names(),
            [
                "INITIALIZE",
                "BASELINE",
                "EXPLORE",
                "REFINE",
                "VERIFY",
                "FINALIZE",
            ],
        )

    def test_protocol_serialization(self):
        protocol = ExperimentProtocol()

        data = protocol.to_dict()

        self.assertEqual(
            data["name"],
            "JAGER Black-Box Discovery Protocol",
        )

        self.assertEqual(
            len(data["steps"]),
            6,
        )

    def test_duplicate_steps_rejected(self):
        protocol = ExperimentProtocol()

        protocol.steps.append(
            protocol.steps[0]
        )

        with self.assertRaises(
            ValueError
        ):
            protocol.validate()


class TestProtocolStateMachine(
    unittest.TestCase
):

    def test_valid_sequence(self):
        machine = ProtocolStateMachine()

        machine.transition(
            ProtocolState.INITIALIZED
        )

        machine.transition(
            ProtocolState.BASELINE
        )

        machine.transition(
            ProtocolState.EXPLORING
        )

        machine.transition(
            ProtocolState.FINALIZED
        )

        self.assertEqual(
            machine.current(),
            "FINALIZED",
        )

    def test_invalid_transition(self):
        machine = ProtocolStateMachine()

        with self.assertRaises(
            ValueError
        ):
            machine.transition(
                ProtocolState.FINALIZED
            )


if __name__ == "__main__":
    unittest.main()
