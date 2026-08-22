import tempfile
import unittest
from pathlib import Path

from .run_store import RunStore


class TestRunStore(unittest.TestCase):

    def test_save_and_load(self):

        with tempfile.TemporaryDirectory() as directory:

            store = RunStore(
                directory=directory
            )

            data = {
                "run_id": "run-test",
                "experiments": 5,
                "discoveries": 1,
            }

            path = store.save(
                "run-test",
                data,
            )

            self.assertTrue(
                Path(path).exists()
            )

            loaded = store.load(
                "run-test"
            )

            self.assertEqual(
                loaded,
                data,
            )

    def test_exists(self):

        with tempfile.TemporaryDirectory() as directory:

            store = RunStore(
                directory=directory
            )

            self.assertFalse(
                store.exists("missing")
            )

            store.save(
                "run-1",
                {"value": 1},
            )

            self.assertTrue(
                store.exists("run-1")
            )

    def test_list_runs(self):

        with tempfile.TemporaryDirectory() as directory:

            store = RunStore(
                directory=directory
            )

            store.save(
                "run-b",
                {},
            )

            store.save(
                "run-a",
                {},
            )

            self.assertEqual(
                store.list_runs(),
                [
                    "run-a",
                    "run-b",
                ],
            )


if __name__ == "__main__":
    unittest.main()
