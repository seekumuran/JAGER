import unittest

from .capability_graph import (
    CapabilityGraph,
)


class TestCapabilityGraph(
    unittest.TestCase
):

    def setUp(self):

        self.graph = CapabilityGraph()

        self.graph.register(
            "linux",
            "system",
            [
                "observe",
                "process_count",
            ],
        )

        self.graph.register(
            "linux",
            "resources",
            [
                "cpu_observation",
                "memory_observation",
            ],
        )

    def test_capabilities(self):

        result = self.graph.capabilities(
            "linux"
        )

        self.assertEqual(
            result,
            [
                "resources",
                "system",
            ],
        )

    def test_operations(self):

        result = self.graph.operations(
            "linux"
        )

        self.assertIn(
            "observe",
            result,
        )

        self.assertIn(
            "cpu_observation",
            result,
        )

    def test_supported_operation(self):

        self.assertTrue(
            self.graph.supports(
                "linux",
                "observe",
            )
        )

    def test_unsupported_operation(self):

        self.assertFalse(
            self.graph.supports(
                "linux",
                "execute_shell",
            )
        )

    def test_unknown_target(self):

        self.assertEqual(
            self.graph.capabilities(
                "unknown"
            ),
            [],
        )


if __name__ == "__main__":
    unittest.main()
