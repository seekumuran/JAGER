import unittest

from ..discovery.discovery_record import (
    DiscoveryRecord,
)

from .discovery_bridge import (
    DiscoveryExperienceBridge,
)

from .experience_manager import (
    ExperienceManager,
)


class TestDiscoveryBridge(
    unittest.TestCase
):

    def test_promotes_discovery(self):

        manager = ExperienceManager()

        bridge = (
            DiscoveryExperienceBridge(
                manager
            )
        )

        discovery = (
            DiscoveryRecord.create(
                experiment_id="exp-001",
                target="mock",
                category="failure",
                severity="medium",
                novelty=0.90,
                confidence=0.95,
            )
        )

        experience = bridge.promote(
            discovery=discovery,
            hypothesis=(
                "High load causes failure."
            ),
            action={
                "type": "probe",
                "load": 90,
            },
            outcome={
                "status": "failure"
            },
        )

        self.assertTrue(
            experience.discovery
        )

        self.assertEqual(
            experience.target,
            "mock",
        )

        self.assertEqual(
            manager.size(),
            1,
        )

        self.assertEqual(
            experience.novelty,
            0.90,
        )

        self.assertEqual(
            experience.confidence,
            0.95,
        )


if __name__ == "__main__":
    unittest.main()
