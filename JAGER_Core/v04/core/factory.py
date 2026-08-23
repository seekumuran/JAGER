from typing import Any, Dict, Optional

from ..runtime.budget_manager import (
    BudgetManager,
)

from ..runtime.experiment_runtime import (
    ExperimentRuntime,
)

from ..runtime.runtime_controller import (
    RuntimeController,
)

from ..runtime.termination import (
    TerminationController,
)

from .config import JagerConfig
from .engine import JagerEngine


class JagerFactory:

    @staticmethod
    def create_config(
        values: Optional[
            Dict[str, Any]
        ] = None,
    ) -> JagerConfig:

        config = JagerConfig.from_dict(
            values or {}
        )

        return config

    @staticmethod
    def create_controller(
        config: JagerConfig,
    ) -> RuntimeController:

        termination = (
            TerminationController(
                target_score=
                    config.target_score,
                maximum_iterations=
                    config.max_iterations,
            )
        )

        budget = BudgetManager()

        return RuntimeController(
            budget=budget,
            termination=termination,
        )

    @classmethod
    def create(
        cls,
        config: Optional[
            JagerConfig
        ] = None,
    ) -> JagerEngine:

        config = (
            config
            or cls.create_config()
        )

        controller = (
            cls.create_controller(
                config
            )
        )

        engine = JagerEngine(
            config=config
        )

        engine.termination = (
            controller.termination
        )

        engine.budget = (
            controller.budget
        )

        return engine
