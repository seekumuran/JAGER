class ExperienceSimilarity:

    FIELDS = (
        "cpu_load",
        "memory_load",
        "num_processes",
        "num_threads",
        "ipc_intensity",
    )

    SCALES = {
        "cpu_load": 100.0,
        "memory_load": 100.0,
        "num_processes": 200.0,
        "num_threads": 400.0,
        "ipc_intensity": 100.0,
    }

    def distance(self, first, second):
        total = 0.0

        for field in self.FIELDS:
            difference = (
                float(first[field])
                - float(second[field])
            )

            scale = self.SCALES[field]

            total += (
                difference / scale
            ) ** 2

        return total ** 0.5

    def similarity(self, first, second):
        distance = self.distance(
            first,
            second,
        )

        return max(
            0.0,
            1.0 - distance,
        )
