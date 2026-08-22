import time

from .base import (
    BaseTarget,
    TargetResult,
)


class AISandboxTarget(BaseTarget):

    name = "ai_sandbox"

    def __init__(
        self,
        max_prompt_length=4096,
    ):

        self.max_prompt_length = (
            max_prompt_length
        )

        self.request_count = 0

    def capabilities(self):

        return [
            "prompt_observation",
            "token_length_observation",
            "request_count",
            "latency_observation",
        ]

    def observe(self, action):

        parameters = action.get(
            "parameters",
            {},
        )

        prompt = parameters.get(
            "prompt",
            "",
        )

        if not isinstance(
            prompt,
            str,
        ):
            return TargetResult(
                target=self.name,
                status="DENIED",
                telemetry={},
                metadata={
                    "reason":
                        "Prompt must be a string"
                },
            )

        if len(prompt) > (
            self.max_prompt_length
        ):
            return TargetResult(
                target=self.name,
                status="DENIED",
                telemetry={
                    "prompt_length":
                        len(prompt),
                },
                metadata={
                    "reason":
                        "Prompt exceeds "
                        "sandbox limit"
                },
            )

        start = time.perf_counter()

        self.request_count += 1

        prompt_length = len(prompt)

        estimated_tokens = (
            prompt_length + 3
        ) // 4

        latency_ms = (
            time.perf_counter()
            - start
        ) * 1000.0

        telemetry = {
            "prompt_length":
                prompt_length,

            "estimated_tokens":
                estimated_tokens,

            "request_count":
                self.request_count,

            "latency_ms":
                latency_ms,
        }

        return TargetResult(
            target=self.name,
            status="NORMAL",
            telemetry=telemetry,
            metadata={
                "operation":
                    "prompt_observation",
            },
        )
