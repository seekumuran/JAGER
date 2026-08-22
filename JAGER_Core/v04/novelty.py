from math import sqrt


class NoveltyDetector:

    def distance(self, first, second):
        keys = [
            "cpu_load",
            "memory_load",
            "num_processes",
            "num_threads",
            "ipc_intensity",
        ]

        total = 0.0

        for key in keys:
            a = float(first[key])
            b = float(second[key])

            if key in {
                "num_processes",
                "num_threads",
            }:
                scale = 400.0
            else:
                scale = 100.0

            total += ((a - b) / scale) ** 2

        return sqrt(total)

    def score(self, inputs, previous):
        if not previous:
            return 1.0

        distances = [
            self.distance(inputs, item)
            for item in previous
        ]

        return min(
            1.0,
            max(distances),
        )
