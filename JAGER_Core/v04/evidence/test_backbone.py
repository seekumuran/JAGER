import unittest

from .backbone import (
    ActionRecord,
    InstrumentedBackbone,
    PolicyEvaluation,
    TargetResponse,
)

from .chain import EvidenceChain


class TestInstrumentedBackbone(
    unittest.TestCase
):

    def test_complete_backbone(self):

        backbone = (
            InstrumentedBackbone()
        )

        policy = (
            backbone.record_policy_evaluation(
                "exp-001",
                PolicyEvaluation(
                    policy_id="policy-safe-v1",
                    decision="ALLOW",
                    reason="Action permitted",
                    allowed=True,
                ),
            )
        )

        decision = (
            backbone.record_decision(
                "exp-001",
                "ALLOW",
                "Policy permitted action",
                policy.event_id,
            )
        )

        action = (
            backbone.record_action(
                "exp-001",
                ActionRecord(
                    action_type="probe",
                    parameters={
                        "x": 10
                    },
                    environment_snapshot_hash=(
                        "sha256:test"
                    ),
                ),
                decision.event_id,
            )
        )

        backbone.record_target_response(
            "exp-001",
            TargetResponse(
                return_value={
                    "status": "ok"
                },
                status="success",
                duration_ms=12.4,
            ),
            action.event_id,
        )

        events = (
            backbone.experiment_events(
                "exp-001"
            )
        )

        chain = EvidenceChain(
            events
        )

        self.assertTrue(
            chain.backbone_complete()
        )

        self.assertEqual(
            chain.missing(),
            [],
        )

    def test_incomplete_backbone(self):

        backbone = (
            InstrumentedBackbone()
        )

        backbone.record_policy_evaluation(
            "exp-002",
            PolicyEvaluation(
                policy_id="policy-v1",
                decision="DENY",
                reason="Blocked",
                allowed=False,
            ),
        )

        chain = EvidenceChain(
            backbone.experiment_events(
                "exp-002"
            )
        )

        self.assertFalse(
            chain.backbone_complete()
        )

        self.assertIn(
            "action",
            chain.missing(),
        )


if __name__ == "__main__":
    unittest.main()
