from typing import Dict, List, Optional

from .experiment import Experiment


class ExperimentManager:

    def __init__(self):

        self._experiments: Dict[
            str,
            Experiment,
        ] = {}

    def create(
        self,
        name: str,
        objective: str,
        target: str,
        metadata: Optional[Dict] = None,
    ) -> Experiment:

        experiment = Experiment(
            name=name,
            objective=objective,
            target=target,
            metadata=dict(
                metadata or {}
            ),
        )

        self._experiments[
            experiment.experiment_id
        ] = experiment

        return experiment

    def get(
        self,
        experiment_id: str,
    ) -> Optional[Experiment]:

        return self._experiments.get(
            experiment_id
        )

    def start(
        self,
        experiment_id: str,
    ):

        experiment = self._require(
            experiment_id
        )

        experiment.start()

        return experiment

    def complete(
        self,
        experiment_id: str,
        result=None,
    ):

        experiment = self._require(
            experiment_id
        )

        experiment.complete(
            result
        )

        return experiment

    def fail(
        self,
        experiment_id: str,
        error,
    ):

        experiment = self._require(
            experiment_id
        )

        experiment.fail(
            error
        )

        return experiment

    def cancel(
        self,
        experiment_id: str,
    ):

        experiment = self._require(
            experiment_id
        )

        experiment.cancel()

        return experiment

    def all(self) -> List[Experiment]:

        return list(
            self._experiments.values()
        )

    def active(self):

        return [
            experiment
            for experiment
            in self._experiments.values()
            if not experiment.is_terminal()
        ]

    def _require(
        self,
        experiment_id: str,
    ) -> Experiment:

        experiment = self.get(
            experiment_id
        )

        if experiment is None:

            raise KeyError(
                f"unknown experiment: "
                f"{experiment_id}"
            )

        return experiment

    def snapshot(self):

        return [
            experiment.to_dict()
            for experiment
            in self._experiments.values()
        ]
