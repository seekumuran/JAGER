import unittest

from .patterns import PatternMiner


class TestPatternMiner(unittest.TestCase):

    def test_failure_region(self):
        miner = PatternMiner()

        inputs = {
            "cpu_load": 80,
            "memory_load": 80,
            "num_processes": 100,
            "num_threads": 200,
            "ipc_intensity": 80,
        }

        miner.observe(
            inputs,
            "FAILED",
        )

        failures = miner.failure_regions()

        self.assertEqual(
            len(failures),
            1,
        )

    def test_normal_region(self):
        miner = PatternMiner()

        inputs = {
            "cpu_load": 20,
            "memory_load": 20,
            "num_processes": 10,
            "num_threads": 20,
            "ipc_intensity": 20,
        }

        miner.observe(
            inputs,
            "NORMAL",
        )

        self.assertEqual(
            len(miner.patterns()),
            1,
        )


if __name__ == "__main__":
    unittest.main()
