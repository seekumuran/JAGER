import unittest

from .target_registry import TargetRegistry


class FakeTarget:

    def observe(self, **inputs):
        return {
            "status": "NORMAL"
        }


class TestTargetRegistry(unittest.TestCase):

    def test_register_and_get(self):
        registry = TargetRegistry()

        target = FakeTarget()

        registry.register(
            "test",
            target,
        )

        self.assertIs(
            registry.get("test"),
            target,
        )

    def test_names(self):
        registry = TargetRegistry()

        registry.register(
            "zeta",
            FakeTarget(),
        )

        registry.register(
            "alpha",
            FakeTarget(),
        )

        self.assertEqual(
            registry.names(),
            [
                "alpha",
                "zeta",
            ],
        )

    def test_unknown_target(self):
        registry = TargetRegistry()

        with self.assertRaises(
            KeyError
        ):
            registry.get("missing")

    def test_remove(self):
        registry = TargetRegistry()

        registry.register(
            "test",
            FakeTarget(),
        )

        registry.remove("test")

        self.assertNotIn(
            "test",
            registry,
        )


if __name__ == "__main__":
    unittest.main()
