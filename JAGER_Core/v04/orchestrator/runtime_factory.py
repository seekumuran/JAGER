from typing import Optional

from ..config.config import (
    JagerConfig,
)

from ..config.defaults import (
    default_config,
)

from ..executor.executor import (
    ExperimentExecutor,
)

from ..executor.registry import (
    TargetRegistry,
)

from ..experience.experience_manager import (
    ExperienceManager,
)

from ..persistence.json_runtime_state_repository import (
    JsonRuntimeStateRepository,
)

from ..persistence.persistent_state_manager import (
    PersistentStateManager,
)

from ..planner.planner import (
    ExperimentPlanner,
)

from ..policy.default_policy import (
    build_default_policy,
)

from ..policy.policy_mediator import (
    PolicyMediator,
)

from ..runtime.experiment_runner import (
    ExperimentRunner,
)

from .jager_orchestrator import (
    JagerOrchestrator,
)

from .persistent_orchestrator import (
    PersistentJagerRuntime,
)


def build_runtime(
    registry: TargetRegistry,
    config: Optional[
        JagerConfig
    ] = None,
    state_path: str = (
        "data/runtime_state.json"
    ),
):

    config = (
        config
        or default_config()
    )

    config.validate()

    executor = ExperimentExecutor(
        registry
    )

    policy = PolicyMediator(
        build_default_policy()
    )

    runner = ExperimentRunner(
        executor=executor,
        policy=policy,
    )

    orchestrator = JagerOrchestrator(
        planner=ExperimentPlanner(),
        runner=runner,
    )

    runtime = PersistentJagerRuntime(
        orchestrator=orchestrator,
        config=config,
        state_path=state_path,
    )

    return runtime
