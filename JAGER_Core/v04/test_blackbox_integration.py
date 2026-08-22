import unittest

from blackbox_system import SimulatedSystem

from .blackbox_adapter import BlackBoxAdapter
from .config import JagerConfig
from .integration import JagerRuntime


class TestBlackBoxIntegration(
    unittest.TestCase
):

    def test_blackbox_can_attach(self):

        simulator = SimulatedSystem(
            seed=42
        )

        target = BlackBoxAdapter(
            simulator
        )

        runtime = JagerRuntime(
            config=JagerConfig(
                seed=42,
                budget=5,
            )
        )

        runtime.attach_target(
            "blackbox",
            target,
        )

        self.assertIn(
            "blackbox",
            runtime.registry,
        )

    def test_blackbox_can_run(self):

        simulator = SimulatedSystem(
            seed=42
        )

        target = BlackBoxAdapter(
            simulator
        )

        runtime = JagerRuntime(
            config=JagerConfig(
                seed=42,
                budget=5,
            )
        )

        runtime.attach_target(
            "blackbox",
            target,
        )

        runtime.start(
            "blackbox"
        )

        self.assertEqual(
            len(
                runtime.hunter.experiments
            ),
            5,
        )

    def test_blackbox_remains_blackbox(self):

        simulator = SimulatedSystem(
            seed=42
        )

        target = BlackBoxAdapter(
            simulator
        )

        result = target.observe(
            cpu_load=50,
            memory_load=50,
            num_processes=50,
            num_threads=100,
            ipc_intensity=50,
        )

        self.assertEqual(
            set(result.keys()),
            {
                "inputs",
                "telemetry",
                "status",
            },
        )

        self.assertNotIn(
            "failure_reason",
            result,
        )

        self.assertNotIn(
            "internal_state",
            result,
        )


if __name__ == "__main__":
    unittest.main()
