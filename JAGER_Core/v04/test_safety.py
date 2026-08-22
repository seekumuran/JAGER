import unittest

from .safety import SafetyController


class TestSafetyController(unittest.TestCase):

    def setUp(self):
        self.controller = SafetyController()

    def valid(self):
        return {
            "cpu_load": 50,
            "memory_load": 50,
            "num_processes": 50,
            "num_threads": 100,
            "ipc_intensity": 50,
        }

    def test_safe_input(self):
        result = self.controller.check(
            self.valid()
        )

        self.assertTrue(result["safe"])
        self.assertEqual(
            result["violations"],
            [],
        )

    def test_cpu_limit(self):
        data = self.valid()
        data["cpu_load"] = 100

        result = self.controller.check(data)

        self.assertFalse(result["safe"])
        self.assertIn(
            "CPU_LIMIT",
            result["violations"],
        )

    def test_thread_limit(self):
        data = self.valid()
        data["num_threads"] = 400

        result = self.controller.check(data)

        self.assertFalse(result["safe"])
        self.assertIn(
            "THREAD_LIMIT",
            result["violations"],
        )


if __name__ == "__main__":
    unittest.main()
