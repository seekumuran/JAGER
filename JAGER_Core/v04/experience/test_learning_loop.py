import unittest

from ..evidence.backbone import (
    ActionRecord,
    InstrumentedBackbone,
    PolicyEvaluation,
    TargetResponse,
)

from ..evidence.chain import (
    EvidenceChain,
)

from .discovery_pipeline import (
    DiscoveryPipeline,
)

from .learning_loop import (
    DiscoveryLearningLoop,
)

from ..experience.experience_manager import (
    ExperienceManager,
)


class TestLearningLoop(
    unittest.TestCase
):

    def _evidence(self):

        backbone = (
            InstrumentedBackbone()
        )

        policy = (
            backbone
            .record_policy_evaluation(
                "exp-001",
                PolicyEvaluation(
                    policy_id="policy-v1",
                    decision="ALLOW",
                    reason="allowed",
                    allowed=True,
                ),
            )
        )

        decision = (
            backbone.record_decision(
                "exp-001",
                "ALLOW",
                "allowed",
                policy.event_id,
            )
        )

        action = (
            backbone.record_action(
                "exp-001",
                ActionRecord(
                    action_type="probe",
                    parameters={
                        "load": 90
                    },
                    environment_snapshot_hash=(
                        "snapshot"
                    ),
                ),
                decision.event_id,
            )
        )

        backbone.record_target_response(
            "exp-001",
            TargetResponse(
                return_value={
                    "status": "failure"
                },
                status="success",
                duration_ms=5.0,
            ),
            action.event_id,
        )

        return EvidenceChain(
            backbone.experiment_events(
                "exp-001"
            )
        )

    def test_discovery_becomes_experience(self):

        pipeline = DiscoveryPipeline()

        manager = ExperienceManager()

        loop = DiscoveryLearningLoop(
            discovery_pipeline=pipeline,
            experience_manager=manager,
        )

        result = loop.process(
            experiment_id="exp-001",
            target="mock",
            hypothesis=(
                "High load causes failure."
            ),
            action={
                "type": "probe",
                "load": 90,
            },
            outcome={
                "status": "failure",
                "confidence": 0.95,
            },
            evidence=self._evidence(),
            baseline={
                "status": "success"
            },
        )

        self.assertIsNotNone(
            result["discovery"]
        )

        self.assertIsNotNone(
            result["experience"]
        )

        self.assertEqual(
            manager.size(),
            1,
        )

        related = loop.retrieve_related(
            target="mock",
            tags=["failure"],
        )

        self.assertEqual(
            len(related),
            1,
        )


if __name__ == "__main__":
    unittest.main()
