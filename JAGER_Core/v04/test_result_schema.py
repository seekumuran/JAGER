import unittest

from .result_schema import (
    ObservationRecord,
    ExperimentRecord,
    RunSummary,
    ExperimentRun,
)


class TestResultSchema(unittest.TestCase):

    def test_run_record(self):

        summary = RunSummary(
            run_id="run-001",
            jager_version="0.4.0",
            target="blackbox",
            seed=42,
            budget=10,
            started_at=100.0,
        )

        run = ExperimentRun(
            summary
        )

        observation = ObservationRecord(
            status="NORMAL",
            telemetry={
                "cpu_usage": 30
            },
            inputs={
                "cpu_load": 25
            },
        )

        record = ExperimentRecord(
            experiment_id="exp-001",
            run_id="run-001",
            sequence=1,
            action={
                "type": "probe"
            },
            observation=observation,
            reward=0.5,
            novelty=0.2,
            timestamp=101.0,
        )

        run.add(record)

        data = run.to_dict()

        self.assertEqual(
            data["summary"]["experiments"],
            1,
        )

        self.assertEqual(
            len(data["records"]),
            1,
        )

        self.assertEqual(
            data["records"][0]
            ["observation"]["status"],
            "NORMAL",
        )


if __name__ == "__main__":
    unittest.main()
