from typing import Any, Dict, Optional

from ..evidence.chain import (
    EvidenceChain,
)

from .discovery_classifier import (
    DiscoveryClassifier,
)

from .discovery_record import (
    DiscoveryRecord,
)

from .discovery_store import (
    DiscoveryStore,
)

from .evidence_validator import (
    DiscoveryEvidenceValidator,
)


class DiscoveryPipeline:

    def __init__(
        self,
        classifier: Optional[
            DiscoveryClassifier
        ] = None,
        store: Optional[
            DiscoveryStore
        ] = None,
    ):

        self.classifier = (
            classifier
            or DiscoveryClassifier()
        )

        self.store = (
            store
            or DiscoveryStore()
        )

        self.validator = (
            DiscoveryEvidenceValidator()
        )

    def process(
        self,
        experiment_id: str,
        target: str,
        observation: Dict[str, Any],
        evidence: EvidenceChain,
        baseline: Optional[
            Dict[str, Any]
        ] = None,
    ):

        classification = (
            self.classifier.classify(
                observation,
                baseline,
            )
        )

        if not classification.is_discovery:

            return None

        if not self.validator.can_support_discovery(
            evidence
        ):

            return None

        event_ids = [
            event.event_id
            for event in evidence.events
        ]

        discovery = (
            DiscoveryRecord.create(
                experiment_id=
                    experiment_id,
                target=target,
                category=
                    classification.category,
                severity=
                    classification.severity,
                novelty=
                    classification.novelty,
                confidence=
                    classification.confidence,
                evidence_event_ids=
                    event_ids,
                description=
                    classification.reason,
                metadata={
                    "classification":
                        classification.to_dict(),
                },
            )
        )

        self.store.add(
            discovery
        )

        return discovery
