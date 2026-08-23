import unittest

from .registry import (
    ComponentRegistry,
)

from .runtime_registry import (
    RuntimeRegistry,
)


class TestComponentRegistry(
    unittest.TestCase
):

    def test_register_and_get(self):

        registry = ComponentRegistry()

        component = object()

        registry.register(
            "test",
            component,
        )

        self.assertIs(
            registry.get("test"),
            component,
        )

        self.assertTrue(
            registry.contains("test")
        )

    def test_duplicate(self):

        registry = ComponentRegistry()

        registry.register(
            "test",
            object(),
        )

        with self.assertRaises(
            KeyError
        ):

            registry.register(
                "test",
                object(),
            )

    def test_remove(self):

        registry = ComponentRegistry()

        registry.register(
            "test",
            object(),
        )

        registry.remove("test")

        self.assertFalse(
            registry.contains("test")
        )


class TestRuntimeRegistry(
    unittest.TestCase
):

    def test_defaults(self):

        registry = RuntimeRegistry()

        self.assertIsNotNone(
            registry.get("budget")
        )

        self.assertIsNotNone(
            registry.get("checkpoint")
        )

        self.assertIsNotNone(
            registry.get("execution")
        )

        self.assertIsNotNone(
            registry.get("experiment")
        )

        self.assertIsNotNone(
            registry.get("iteration")
        )

        self.assertIsNotNone(
            registry.get("session")
        )


if __name__ == "__main__":
    unittest.main()
