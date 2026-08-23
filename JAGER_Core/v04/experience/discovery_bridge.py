from typing import Optional

from ..discovery.discovery_record import (
    DiscoveryRecord,
)

from .experience_manager import (
    ExperienceManager,
)

from .experience_record import (
    ExperienceRecord,
)


class DiscoveryExperienceBridge:

    def __init__(
        self,
        experience_manager: ExperienceManager,
    ):

        self.experience_manager = (
            experience_manager
        )

    def promote(
        self,
        discovery: DiscoveryRecord,
        hypothesis: str,
        action: dict,
        outcome: dict,
        parent_experience_id: Optional[
            str
        ] = None,
    ):

        experience = (
            ExperienceRecord.create(
                target=discovery.target,
                hypothesis=hypothesis,
                action=action,
                outcome=outcome,
                discovery=True,
                novelty=discovery.novelty,
                confidence=discovery.confidence,
                tags=[
                    discovery.category,
                    discovery.severity,
                    "discovery",
                ],
                parent_experience_id=(
                    parent_experience_id
                ),
            )
        )

        self.experience_manager.add(
            experience
        )

        return experience
