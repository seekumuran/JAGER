from typing import Any

from .registry import (
    ComponentRegistry,
)

from .budget_manager import (
    BudgetManager,
)

from .checkpoint_manager import (
    CheckpointManager,
)

from .execution_manager import (
    ExecutionManager,
)

from .experiment_manager import (
    ExperimentManager,
)

from .iteration_manager import (
    IterationManager,
)

from .session_manager import (
    SessionManager,
)


class RuntimeRegistry:

    def __init__(self):

        self.components = (
            ComponentRegistry()
        )

        self.register_defaults()

    def register_defaults(self):

        self.components.register(
            "budget",
            BudgetManager(),
        )

        self.components.register(
            "checkpoint",
            CheckpointManager(
                store=None
            ),
            replace=True,
        )

        self.components.register(
            "execution",
            ExecutionManager(),
        )

        self.components.register(
            "experiment",
            ExperimentManager(),
        )

        self.components.register(
            "iteration",
            IterationManager(),
        )

        self.components.register(
            "session",
            SessionManager(),
        )

    def register(
        self,
        name: str,
        component: Any,
        *,
        replace: bool = False,
    ):

        return self.components.register(
            name,
            component,
            replace=replace,
        )

    def get(
        self,
        name: str,
    ):

        return self.components.get(
            name
        )

    def require(
        self,
        name: str,
    ):

        return self.components.require(
            name
        )

    def snapshot(self):

        return self.components.snapshot()
