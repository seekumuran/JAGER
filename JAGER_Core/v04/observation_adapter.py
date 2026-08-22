from .models import Observation
from .observation_validator import (
    validate_observation,
)


class ObservationAdapter:

    def convert(
        self,
        action_id,
        result,
        timestamp,
    ):
        validate_observation(result)

        return Observation(
            observation_id="",
            action_id=action_id,
            telemetry=result["telemetry"],
            status=result["status"],
            timestamp=timestamp,
        )
