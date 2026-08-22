from .experiment_logger import ExperimentLogger
from .experiment_metrics import ExperimentMetrics


class ExperimentController:

    def __init__(
        self,
        hunter,
        logger=None,
        metrics=None,
    ):
        self.hunter = hunter

        self.logger = (
            logger
            or ExperimentLogger()
        )

        self.metrics = (
            metrics
            or ExperimentMetrics()
        )

        self.started = False
        self.completed = False
        self.stopped = False

    def start(self):
        if self.started:
            raise RuntimeError(
                "Experiment controller "
                "has already started."
            )

        self.started = True
        self.completed = False
        self.stopped = False

        return self.run()

    def run(self):
        if not self.started:
            self.started = True

        results = []

        for _ in range(
            self.hunter.budget
        ):
            if self.stopped:
                break

            result = (
                self.hunter.run_experiment()
            )

            results.append(result)

        self.completed = True

        return results

    def stop(self):
        self.stopped = True

    def progress(self):
        completed = len(
            self.hunter.experiments
        )

        budget = self.hunter.budget

        percentage = (
            completed / budget * 100
            if budget > 0
            else 0.0
        )

        return {
            "completed": completed,
            "budget": budget,
            "percentage": percentage,
            "started": self.started,
            "completed_run":
                self.completed,
            "stopped": self.stopped,
        }
