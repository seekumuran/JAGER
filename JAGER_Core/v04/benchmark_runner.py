from .benchmark import Benchmark


class BenchmarkRunner:

    def __init__(
        self,
        runtime,
        target_name,
    ):
        self.runtime = runtime
        self.target_name = target_name

    def run(self):

        result = self.runtime.run_protocol(
            self.target_name,
            save=False,
        )

        pipeline = (
            self.runtime
            .controller
            .discovery_pipeline
        )

        benchmark = Benchmark(
            self.runtime.hunter,
            pipeline,
        )

        metrics = benchmark.evaluate()

        return {
            "protocol": result,
            "benchmark": metrics.to_dict(),
        }
