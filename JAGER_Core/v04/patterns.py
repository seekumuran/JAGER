from collections import defaultdict


class PatternMiner:

    def __init__(self):
        self.status_patterns = defaultdict(
            lambda: {
                "count": 0,
                "failures": 0,
                "degraded": 0,
                "normal": 0,
            }
        )

    def observe(
        self,
        inputs,
        status,
    ):
        key = self._bucket(inputs)

        record = self.status_patterns[key]

        record["count"] += 1

        if status == "FAILED":
            record["failures"] += 1
        elif status == "DEGRADED":
            record["degraded"] += 1
        else:
            record["normal"] += 1

    def _bucket(self, inputs):
        cpu = int(
            inputs["cpu_load"] // 20
        )

        memory = int(
            inputs["memory_load"] // 20
        )

        ipc = int(
            inputs["ipc_intensity"] // 20
        )

        processes = int(
            inputs["num_processes"] // 40
        )

        threads = int(
            inputs["num_threads"] // 80
        )

        return (
            cpu,
            memory,
            ipc,
            processes,
            threads,
        )

    def patterns(self):
        return dict(
            self.status_patterns
        )

    def failure_regions(self):
        return {
            key: value
            for key, value
            in self.status_patterns.items()
            if value["failures"] > 0
        }
