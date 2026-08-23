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

from .discovery_classifier import (
    DiscoveryClassifier,
)

from .discovery_pipeline import (
    DiscoveryPipeline,
)


class TestDiscovery(
    unittest.TestCase
):

    def _complete_chain(self):

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
                        "load": 80
                    },
                    environment_snapshot_hash=(
                        "snapshot-1"
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
                duration_ms=10.0,
            ),
            action.event_id,
        )

        return EvidenceChain(
            backbone.experiment_events(
                "exp-001"
            )
        )

    def test_classifier_detects_failure(self):

        classifier = (
            DiscoveryClassifier()
        )

        result = classifier.classify(
            {
                "status": "failure",
                "confidence": 0.95,
            },
            {
                "status": "success",
            },
        )

        self.assertTrue(
            result.is_discovery
        )

        self.assertEqual(
            result.category,
            "failure",
        )

    def test_pipeline_requires_evidence(self):

        pipeline = DiscoveryPipeline()

        chain = EvidenceChain([])

        result = pipeline.process(
            experiment_id="exp-001",
            target="mock",
            observation={
                "status": "failure",
                "confidence": 0.95,
            },
            evidence=chain,
        )

        self.assertIsNone(
            result
        )

    def test_pipeline_creates_discovery(self):

        pipeline = DiscoveryPipeline()

        chain = self._complete_chain()

        result = pipeline.process(
            experiment_id="exp-001",
            target="mock",
            observation={
                "status": "failure",
                "confidence": 0.95,
            },
            evidence=chain,
            baseline={
                "status": "success"
            },
        )

        self.assertIsNotNone(
            result
        )

        self.assertEqual(
            pipeline.store.size(),
            1,
        )

        self.assertEqual(
            result.experiment_id,
            "exp-001",
        )

        self.assertTrue(
            len(
                result.evidence_event_ids
            ) > 0
        )


if __name__ == "__main__":
    unittest.main()
