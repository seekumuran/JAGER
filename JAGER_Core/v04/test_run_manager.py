import tempfile
import unittest

from .result_schema import (
    RunSummary,
    ExperimentRun,
)

from .run_manager import (
    RunManager,
)


class TestRunManager(unittest.TestCase):

    def test_save_and_load(self):

        with tempfile.TemporaryDirectory() as directory:

            manager = RunManager(
                directory
            )

            run = ExperimentRun(
                RunSummary(
                    run_id="run-test",
                    jager_version="0.4.0",
                    target="blackbox",
                    seed=42,
                    budget=5,
                )
            )

            run.finalize()

            path = manager.save(
                run
            )

            self.assertTrue(
                path.exists()
            )

            loaded = manager.load(
                path.name
            )

            self.assertEqual(
                loaded["summary"]["run_id"],
                "run-test",
            )

    def test_list_runs(self):

        with tempfile.TemporaryDirectory() as directory:

            manager = RunManager(
                directory
            )

            run = ExperimentRun(
                RunSummary(
                    run_id="run-test",
                    jager_version="0.4.0",
                    target="blackbox",
                    seed=42,
                    budget=5,
                )
            )

            manager.save(run)

            runs = manager.list_runs()

            self.assertEqual(
                len(runs),
                1,
            )


if __name__ == "__main__":
    unittest.main()
