import unittest

from .telemetry_snapshot import (
    SnapshotStore,
)


class TestSnapshotStore(
    unittest.TestCase
):

    def test_add_snapshot(self):

        store = SnapshotStore()

        snapshot = store.add(
            target="linux",
            experiment_id="exp-001",
            status="NORMAL",
            telemetry={
                "cpu": 42.0,
            },
        )

        self.assertEqual(
            snapshot.target,
            "linux",
        )

        self.assertEqual(
            store.count(),
            1,
        )

    def test_latest(self):

        store = SnapshotStore()

        store.add(
            "linux",
            "exp-001",
            "NORMAL",
            {"cpu": 20.0},
        )

        store.add(
            "linux",
            "exp-002",
            "NORMAL",
            {"cpu": 40.0},
        )

        latest = store.latest(
            "linux"
        )

        self.assertEqual(
            latest.experiment_id,
            "exp-002",
        )

    def test_target_filter(self):

        store = SnapshotStore()

        store.add(
            "linux",
            "exp-001",
            "NORMAL",
            {},
        )

        store.add(
            "blackbox",
            "exp-002",
            "NORMAL",
            {},
        )

        self.assertEqual(
            store.count("linux"),
            1,
        )

        self.assertEqual(
            store.count("blackbox"),
            1,
        )

    def test_max_size(self):

        store = SnapshotStore(
            max_snapshots=2
        )

        for index in range(5):

            store.add(
                "linux",
                f"exp-{index}",
                "NORMAL",
                {},
            )

        self.assertEqual(
            store.count(),
            2,
        )

        self.assertEqual(
            store.latest().experiment_id,
            "exp-4",
        )

    def test_clear(self):

        store = SnapshotStore()

        store.add(
            "linux",
            "exp-001",
            "NORMAL",
            {},
        )

        store.clear()

        self.assertEqual(
            store.count(),
            0,
        )

        self.assertIsNone(
            store.latest()
        )


if __name__ == "__main__":
    unittest.main()
