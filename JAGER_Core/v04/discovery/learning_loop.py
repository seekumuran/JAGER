from typing import Any, Dict, Optional

from .discovery_pipeline import (
    DiscoveryPipeline,
)

from ..experience.discovery_bridge import (
    DiscoveryExperienceBridge,
)

from ..experience.experience_manager import (
    ExperienceManager,
)


class DiscoveryLearningLoop:

    def __init__(
        self,
        discovery_pipeline:
            DiscoveryPipeline,
        experience_manager:
            ExperienceManager,
    ):

        self.discovery_pipeline = (
            discovery_pipeline
        )

        self.experience_manager = (
            experience_manager
        )

        self.bridge = (
            DiscoveryExperienceBridge(
                experience_manager
            )
        )

    def process(
        self,
        experiment_id: str,
        target: str,
        hypothesis: str,
        action: Dict[str, Any],
        outcome: Dict[str, Any],
        evidence,
        baseline: Optional[
            Dict[str, Any]
        ] = None,
    ):

        discovery = (
            self.discovery_pipeline.process(
                experiment_id=experiment_id,
                target=target,
                observation=outcome,
                evidence=evidence,
                baseline=baseline,
            )
        )

        if discovery is None:
            return {
                "discovery": None,
                "experience": None,
            }

        experience = (
            self.bridge.promote(
                discovery=discovery,
                hypothesis=hypothesis,
                action=action,
                outcome=outcome,
            )
        )

        return {
            "discovery": discovery,
            "experience": experience,
        }

    def retrieve_related(
        self,
        target: str,
        tags=None,
        limit: int = 5,
    ):

        return (
            self.experience_manager.retrieve(
                target=target,
                tags=tags,
                limit=limit,
            )
        )
