import random
import uuid

from .learning import ExperienceEvaluator
from .memory import ExperienceMemory
from .observability import EventLogger
from .reasoner import HunterReasoner
from .security import SecurityGate
from .target import SimulatedTarget


class JagerHunter:
    def __init__(
        self,
        seed: int = 42,
        budget: int = 1000,
    ):
        self.seed = seed
        self.budget = budget

        self.rng = random.Random(seed)

        self.run_id = f"run-{uuid.uuid4().hex[:12]}"

        self.target = SimulatedTarget(seed)
        self.memory = ExperienceMemory()
        self.reasoner = HunterReasoner(self.rng)
        self.security = SecurityGate()
        self.logger = EventLogger()
        self.evaluator = ExperienceEvaluator()

        self.experiments = []
        self.failed_discoveries = []

        self.exploration_rate = 0.45

    def run(self):
        previous_status = None

        for number in range(1, self.budget + 1):
            trace_id = f"trace-{uuid.uuid4().hex[:12]}"

            action = self.reasoner.propose(
                self.memory,
                self.exploration_rate,
            )

            self.logger.emit(
                trace_id=trace_id,
                event_type="ACTION_PROPOSED",
                operation=action.operation,
                decision="PENDING",
                reason="HUNTER_PROPOSED_ACTION",
                metadata={
                    "action_id": action.action_id,
                    "experiment": number,
                },
            )

            decision = self.security.authorize(action)

            if not decision.allowed:
                self.logger.emit(
                    trace_id=trace_id,
                    event_type="SECURITY_DECISION",
                    operation=action.operation,
                    decision="DENY",
                    reason=decision.reason,
                )

                continue

            self.logger.emit(
                trace_id=trace_id,
                event_type="SECURITY_DECISION",
                operation=action.operation,
                decision="ALLOW",
                reason=decision.reason,
            )

            observation = self.target.execute(action)

            self.logger.emit(
                trace_id=trace_id,
                event_type="OBSERVATION",
                operation=action.operation,
                decision="ALLOW",
                reason=observation.status,
                metadata=observation.telemetry,
            )

            experience = self.evaluator.evaluate(
                action=action,
                observation=observation,
                previous_status=previous_status,
            )

            self.memory.store(experience)

            self.experiments.append(
                {
                    "experiment": number,
                    "action": action,
                    "observation": observation,
                    "experience": experience,
                }
            )

            previous_status = observation.status

            if observation.status == "FAILED":
                self.failed_discoveries.append(
                    experience
                )

                self.exploration_rate = max(
                    0.15,
                    self.exploration_rate - 0.05,
                )

            else:
                self.exploration_rate = min(
                    0.80,
                    self.exploration_rate + 0.005,
                )

        return self.failed_discoveries
