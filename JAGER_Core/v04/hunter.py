import random
import time

from .action_space import ActionSpace
from .constants import (
    STRATEGY_EXPLORE,
    STRATEGY_EXPLOIT,
)
from .decision import Decision
from .errors import UnsafeActionError
from .experiment_id import (
    generate_experiment_id,
    generate_run_id,
    generate_trace_id,
)
from .experiment_logger import ExperimentLogger
from .experiment_metrics import ExperimentMetrics
from .experience import (
    Experience,
    ExperienceStore,
)
from .knowledge import KnowledgeBase
from .knowledge_update import KnowledgeUpdater
from .models import Action, Observation
from .novelty import NoveltyDetector
from .patterns import PatternMiner
from .reward_model import RewardModel
from .safety import SafetyController
from .strategy import SearchStrategy
from .validation import validate_inputs


class JagerHunter:

    def __init__(
        self,
        seed=42,
        budget=100,
        target=None,
        exploration_rate=0.30,
        memory_capacity=1000,
    ):
        self.seed = seed
        self.budget = budget
        self.target = target

        self.rng = random.Random(seed)

        self.run_id = generate_run_id()

        self.action_space = ActionSpace()

        self.safety = SafetyController()

        self.strategy = SearchStrategy(
            self.rng
        )

        self.novelty = NoveltyDetector()

        self.reward_model = RewardModel()

        self.memory = ExperienceStore(
            capacity=memory_capacity
        )

        self.logger = ExperimentLogger()

        self.metrics = ExperimentMetrics()

        self.knowledge = KnowledgeBase()

        self.knowledge_updater = (
            KnowledgeUpdater(
                self.knowledge
            )
        )

        self.patterns = PatternMiner()

        self.experiments = []

        self.failed_discoveries = []

        self.exploration_rate = (
            exploration_rate
        )

        self.counter = 0

    # --------------------------------------------------
    # Target
    # --------------------------------------------------

    def attach_target(self, target):
        self.target = target

    def require_target(self):
        if self.target is None:
            raise RuntimeError(
                "JÄGER has no target attached."
            )

    # --------------------------------------------------
    # Action generation
    # --------------------------------------------------

    def generate_action(self, strategy):
        if strategy == STRATEGY_EXPLORE:
            return self._random_action()

        return self._informed_action()

    def _random_action(self):
        return {
            "cpu_load": self.rng.uniform(
                0,
                100,
            ),
            "memory_load": self.rng.uniform(
                0,
                100,
            ),
            "num_processes": self.rng.randint(
                0,
                200,
            ),
            "num_threads": self.rng.randint(
                0,
                400,
            ),
            "ipc_intensity": self.rng.uniform(
                0,
                100,
            ),
        }

    def _informed_action(self):
        failures = (
            self.knowledge.all()
        )

        if not failures:
            return self._random_action()

        latest = failures[-1]

        inputs = latest.evidence.get(
            "inputs"
        )

        if not inputs:
            return self._random_action()

        candidate = dict(inputs)

        field = self.rng.choice(
            list(candidate.keys())
        )

        if field in (
            "cpu_load",
            "memory_load",
            "ipc_intensity",
        ):
            candidate[field] = max(
                0,
                min(
                    100,
                    candidate[field]
                    + self.rng.uniform(
                        -10,
                        10,
                    ),
                ),
            )

        elif field == "num_processes":
            candidate[field] = max(
                0,
                min(
                    200,
                    candidate[field]
                    + self.rng.randint(
                        -20,
                        20,
                    ),
                ),
            )

        elif field == "num_threads":
            candidate[field] = max(
                0,
                min(
                    400,
                    candidate[field]
                    + self.rng.randint(
                        -40,
                        40,
                    ),
                ),
            )

        return candidate

    # --------------------------------------------------
    # Safety
    # --------------------------------------------------

    def check_safety(self, inputs):
        return self.safety.check(
            inputs
        )

    # --------------------------------------------------
    # Target execution
    # --------------------------------------------------

    def execute(self, action):
        self.require_target()

        result = self.target.observe(
            **action.parameters
        )

        return result

    # --------------------------------------------------
    # Experiment
    # --------------------------------------------------

    def run_experiment(self):
        self.counter += 1

        experiment_id = (
            generate_experiment_id(
                self.counter
            )
        )

        trace_id = generate_trace_id()

        strategy = self.strategy.choose(
            self.exploration_rate
        )

        parameters = self.generate_action(
            strategy
        )

        validate_inputs(
            parameters
        )

        safety_result = self.check_safety(
            parameters
        )

        action = Action(
            action_id=experiment_id,
            operation="observe",
            parameters=parameters,
        )

        self.logger.action(
            experiment_id,
            trace_id,
            action,
        )

        self.metrics.record_action()

        if not safety_result["safe"]:
            decision = Decision(
                action_id=experiment_id,
                allowed=False,
                reason=(
                    "Safety limits exceeded: "
                    + ", ".join(
                        safety_result[
                            "violations"
                        ]
                    )
                ),
                risk=1.0,
                confidence=1.0,
            )

            self.logger.decision(
                experiment_id,
                trace_id,
                decision,
            )

            self.metrics.record_failure()

            return {
                "experiment_id": experiment_id,
                "trace_id": trace_id,
                "strategy": strategy,
                "action": action,
                "decision": decision,
                "observation": None,
            }

        result = self.execute(action)

        observation = Observation(
            observation_id=(
                f"obs-{self.counter:08d}"
            ),
            action_id=experiment_id,
            telemetry=result["telemetry"],
            status=result["status"],
            timestamp=time.time(),
        )

        self.logger.observation(
            experiment_id,
            trace_id,
            observation,
        )

        decision = Decision(
            action_id=experiment_id,
            allowed=True,
            reason="Target observation allowed.",
            risk=0.0,
            confidence=1.0,
        )

        self.logger.decision(
            experiment_id,
            trace_id,
            decision,
        )

        novelty = self.novelty.score(
            parameters,
            [
                experience.action.parameters
                for experience
                in self.memory.items
            ],
        )

        confirmed = (
            result["status"] == "FAILED"
        )

        reward = self.reward_model.calculate(
            result["status"],
            novelty,
            confirmed=confirmed,
        )

        experience = Experience(
            observation_id=(
                observation.observation_id
            ),
            action=action,
            observation=observation,
            reward=reward,
            novelty=novelty,
            useful=(
                result["status"]
                != "NORMAL"
            ),
        )

        self.memory.add(
            experience
        )

        self.knowledge_updater.update(
            parameters,
            result["status"],
            min(
                1.0,
                0.5 + novelty * 0.5,
            ),
        )

        self.patterns.observe(
            parameters,
            result["status"],
        )

        self.metrics.record_novelty(
            novelty
        )

        self.metrics.record_reward(
            reward
        )

        if result["status"] == "FAILED":
            self.metrics.record_failure()

            self.failed_discoveries.append(
                {
                    "experiment_id":
                        experiment_id,
                    "trace_id":
                        trace_id,
                    "inputs":
                        dict(parameters),
                    "telemetry":
                        dict(
                            result["telemetry"]
                        ),
                    "reward":
                        reward,
                    "novelty":
                        novelty,
                }
            )

        elif result["status"] == "DEGRADED":
            self.metrics.record_degraded()

        else:
            self.metrics.record_normal()

        self.exploration_rate = (
            self.strategy.adjust(
                self.exploration_rate,
                result["status"]
                != "NORMAL",
            )
        )

        record = {
            "experiment_id":
                experiment_id,
            "trace_id":
                trace_id,
            "strategy":
                strategy,
            "action":
                action,
            "decision":
                decision,
            "observation":
                observation,
            "experience":
                experience,
        }

        self.experiments.append(
            record
        )

        return record

    # --------------------------------------------------
    # Main loop
    # --------------------------------------------------

    def run(self):
        self.require_target()

        discoveries = []

        for _ in range(self.budget):
            result = self.run_experiment()

            if result.get(
                "observation"
            ) is not None:

                if (
                    result[
                        "observation"
                    ].status
                    == "FAILED"
                ):
                    discoveries.append(
                        result
                    )

        return discoveries

    # --------------------------------------------------
    # State
    # --------------------------------------------------

    def state(self):
        return {
            "run_id": self.run_id,
            "seed": self.seed,
            "budget": self.budget,
            "target_attached":
                self.target is not None,
            "experiments":
                len(self.experiments),
            "memory":
                len(self.memory),
            "discoveries":
                len(
                    self.failed_discoveries
                ),
            "exploration_rate":
                self.exploration_rate,
            "metrics":
                self.metrics.summary(),
        }
