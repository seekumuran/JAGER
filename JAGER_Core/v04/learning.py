from .models import Experience


class ExperienceEvaluator:
    def evaluate(
        self,
        action,
        observation,
        previous_status=None,
    ) -> Experience:

        reward = 0.0

        if observation.status == "FAILED":
            reward = 10.0
        elif observation.status == "DEGRADED":
            reward = 2.0
        else:
            reward = 0.1

        novelty = 1.0

        if previous_status == observation.status:
            novelty = 0.2

        useful = (
            observation.status in {
                "FAILED",
                "DEGRADED",
            }
        )

        return Experience(
            observation_id=observation.observation_id,
            action=action,
            observation=observation,
            reward=reward,
            novelty=novelty,
            useful=useful,
        )
