import random


class ActionGenerator:

    def __init__(
        self,
        seed=42,
    ):
        self.random = random.Random(
            seed
        )

    def generate(
        self,
        target_name,
    ):

        if target_name == "blackbox":

            return self._blackbox()

        if target_name == "linux":

            return {
                "type": "observe",
                "parameters": {},
            }

        if target_name == "ai_sandbox":

            return self._sandbox()

        raise ValueError(
            f"Unsupported target: "
            f"{target_name}"
        )

    def _blackbox(self):

        return {
            "type": "probe",
            "parameters": {
                "cpu_load":
                    self.random.uniform(
                        0,
                        100,
                    ),

                "memory_load":
                    self.random.uniform(
                        0,
                        100,
                    ),

                "num_processes":
                    self.random.randint(
                        1,
                        300,
                    ),

                "num_threads":
                    self.random.randint(
                        1,
                        600,
                    ),

                "ipc_intensity":
                    self.random.uniform(
                        0,
                        100,
                    ),
            },
        }

    def _sandbox(self):

        operations = [
            "summarize",
            "read_context",
            "classify",
            "generate",
            "inspect",
            "execute_shell",
        ]

        operation = self.random.choice(
            operations
        )

        return {
            "type": "action",
            "parameters": {
                "operation": operation,
                "payload": {},
            },
        }
