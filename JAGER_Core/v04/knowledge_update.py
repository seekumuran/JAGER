from .knowledge import KnowledgeBase


class KnowledgeUpdater:

    def __init__(self, knowledge=None):
        self.knowledge = (
            knowledge or KnowledgeBase()
        )

    def update(
        self,
        inputs,
        status,
        confidence,
    ):
        key = self._key(inputs)

        if status == "FAILED":
            pattern = "failure_region"

        elif status == "DEGRADED":
            pattern = "degradation_region"

        else:
            pattern = "normal_region"

        return self.knowledge.add(
            key=key,
            pattern=pattern,
            evidence={
                "inputs": dict(inputs),
                "status": status,
            },
            confidence=confidence,
        )

    def _key(self, inputs):
        return (
            int(inputs["cpu_load"] // 10),
            int(inputs["memory_load"] // 10),
            int(inputs["ipc_intensity"] // 10),
            int(inputs["num_processes"] // 20),
            int(inputs["num_threads"] // 40),
        )
