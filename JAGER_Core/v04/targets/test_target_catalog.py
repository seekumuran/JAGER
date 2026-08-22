import unittest

from .target_catalog import (
    TargetCatalog,
    TargetDescriptor,
)


class TestTargetCatalog(
    unittest.TestCase
):

    def test_register_target(self):

        catalog = TargetCatalog()

        descriptor = TargetDescriptor(
            name="linux",
            version="1.0",
            description=(
                "Safe Linux observation target"
            ),
            environment="local",
            capabilities=[
                "system_observation",
                "process_count",
            ],
        )

        catalog.add(descriptor)

        self.assertTrue(
            catalog.exists("linux")
        )

        self.assertEqual(
            catalog.get(
                "linux"
            ).version,
            "1.0",
        )

    def test_names(self):

        catalog = TargetCatalog()

        catalog.add(
            TargetDescriptor(
                "linux",
                "1.0",
                "Linux target",
                "local",
                [],
            )
        )

        catalog.add(
            TargetDescriptor(
                "ai_sandbox",
                "1.0",
                "AI sandbox",
                "isolated",
                [],
            )
        )

        self.assertEqual(
            catalog.names(),
            [
                "ai_sandbox",
                "linux",
            ],
        )

    def test_unknown_target(self):

        catalog = TargetCatalog()

        self.assertFalse(
            catalog.exists(
                "unknown"
            )
        )


if __name__ == "__main__":
    unittest.main()
