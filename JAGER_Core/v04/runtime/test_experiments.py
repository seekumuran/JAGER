import tempfile
import unittest

from .experiment_manager import (
    ExperimentManager,
)

from .experiment_store import (
    ExperimentStore,
)


class TestExperimentManager(
    unittest.TestCase
):

    def test_lifecycle(self):

        manager = ExperimentManager()

        experiment = manager.create(
            name="baseline",
            objective="evaluate target",
            target="mock",
        )

        self.assertEqual(
            experiment.status,
            "created",
        )

        manager.start(
            experiment.experiment_id
        )

        self.assertEqual(
            experiment.status,
            "running",
        )

        manager.complete(
            experiment.experiment_id,
            result={
                "score": 0.95
            },
        )

        self.assertEqual(
            experiment.status,
            "completed",
        )

        self.assertTrue(
            experiment.is_terminal()
        )

    def test_active_experiments(self):

        manager = ExperimentManager()

        first = manager.create(
            name="first",
            objective="test",
            target="mock",
        )

        second = manager.create(
            name="second",
            objective="test",
            target="mock",
        )

        manager.start(
            first.experiment_id
        )

        manager.complete(
            first.experiment_id
        )

        self.assertEqual(
            len(manager.active()),
            1,
        )

        self.assertIs(
            manager.active()[0],
            second,
        )


class TestExperimentStore(
    unittest.TestCase
):

    def test_store(self):

        with tempfile.TemporaryDirectory() as tmp:

            manager = ExperimentManager()

            manager.create(
                name="experiment",
                objective="test",
                target="mock",
            )

            store = ExperimentStore(
                f"{tmp}/experiments.json"
            )

            store.save(
                manager.all()
            )

            data = store.load()

            self.assertEqual(
                len(data),
                1,
            )

            self.assertEqual(
                data[0]["name"],
                "experiment",
            )


if __name__ == "__main__":
    unittest.main()
