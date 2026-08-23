import unittest

from .mock_target_adapter import (
    MockTargetAdapter,
)

from .target_registry import (
    TargetRegistry,
)


class TestTargetRegistry(
    unittest.TestCase
):

    def test_register_and_get(self):

        registry = TargetRegistry()

        target = MockTargetAdapter(
            "mock"
        )

        registry.register(target)

        self.assertTrue(
            registry.contains("mock")
        )

        self.assertEqual(
            registry.get("mock"),
            target,
        )

        self.assertEqual(
            registry.size(),
            1,
        )

    def test_names(self):

        registry = TargetRegistry()

        registry.register(
            MockTargetAdapter("zulu")
        )

        registry.register(
            MockTargetAdapter("alpha")
        )

        self.assertEqual(
            registry.names(),
            [
                "alpha",
                "zulu",
            ],
        )

    def test_duplicate_registration(self):

        registry = TargetRegistry()

        registry.register(
            MockTargetAdapter("mock")
        )

        with self.assertRaises(
            ValueError
        ):

            registry.register(
                MockTargetAdapter("mock")
            )

    def test_require(self):

        registry = TargetRegistry()

        with self.assertRaises(
            KeyError
        ):

            registry.require(
                "missing"
            )

    def test_unregister(self):

        registry = TargetRegistry()

        registry.register(
            MockTargetAdapter("mock")
        )

        removed = registry.unregister(
            "mock"
        )

        self.assertIsNotNone(
            removed
        )

        self.assertFalse(
            registry.contains("mock")
        )

    def test_adapter_contract(self):

        target = MockTargetAdapter(
            "mock"
        )

        result = target.execute(
            action_type="probe",
            parameters={
                "intensity": 0.25
            },
        )

        self.assertEqual(
            result["status"],
            "success",
        )

        self.assertEqual(
            result["target"],
            "mock",
        )


if __name__ == "__main__":
    unittest.main()
