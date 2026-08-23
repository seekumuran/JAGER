from typing import Iterable

from ..evidence.chain import (
    EvidenceChain,
)


class DiscoveryEvidenceValidator:

    def validate(
        self,
        chain: EvidenceChain,
    ):

        missing = chain.missing()

        return {
            "valid": (
                len(missing) == 0
            ),
            "backbone_complete":
                chain.backbone_complete(),
            "missing":
                missing,
        }

    def can_support_discovery(
        self,
        chain: EvidenceChain,
    ):

        result = self.validate(
            chain
        )

        return result[
            "backbone_complete"
        ]
