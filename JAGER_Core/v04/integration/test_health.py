import unittest

from ..api.jager import (
    Jager,
)

from ..executor.mock_target_adapter import (
    MockTargetAdapter,
)

from ..executor.target_registry import (
    TargetRegistry,
)

from .health_check import (
    HealthChecker,
)

from .system_health import (
    SystemHealth,
)

from .integration_status import (
    IntegrationStatus,
)


class TestHealthChecker(
    unittest.TestCase
):

    def test_healthy_component(self):

        checker = HealthChecker()

        result = checker.check_component(
            "planner",
            True,
        )

        self.assertTrue(
            result.healthy
        )

        self.assertEqual(
            result.component,
            "planner",
        )

    def test_unhealthy_component(self):

        checker = HealthChecker()

        result = checker.check_component(
            "executor",
            False,
        )

        self.assertFalse(
            result.healthy
        )

    def test_all(self):

        checker = HealthChecker()

        components = {
            "planner": True,
            "executor": True,
            "target": False,
        }

        self.assertFalse(
            checker.healthy(
                components
            )
        )


class TestSystemHealth(
    unittest.TestCase
):

    def _jager(self):

        registry = TargetRegistry()

        registry.register(
            MockTargetAdapter(
                "mock"
            )
        )

        return Jager(
            registry=registry
        )

    def test_health(self):

        jager = self._jager()

        health = SystemHealth(
            jager
        )

        result = health.check()

        self.assertIn(
            "healthy",
            result,
        )

        self.assertIn(
            "components",
            result,
        )

        self.assertTrue(
            result["healthy"]
        )


class TestIntegrationStatus(
    unittest.TestCase
):

    def test_snapshot(self):

        registry = TargetRegistry()

        registry.register(
            MockTargetAdapter(
                "mock"
            )
        )

        jager = Jager(
            registry=registry
        )

        status = IntegrationStatus(
            jager
        ).snapshot()

        self.assertEqual(
            status["target_count"],
            1,
        )

        self.assertIn(
            "runtime",
            status,
        )


if __name__ == "__main__":
    unittest.main()
