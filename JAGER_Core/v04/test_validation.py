import unittest

from .validation import validate_inputs


class TestValidation(unittest.TestCase):

    def valid(self):
        return {
            "cpu_load": 50.0,
            "memory_load": 50.0,
            "num_processes": 50,
            "num_threads": 100,
            "ipc_intensity": 50.0,
        }

    def test_valid_input(self):
        self.assertTrue(
            validate_inputs(self.valid())
        )

    def test_invalid_cpu(self):
        data = self.valid()
        data["cpu_load"] = 101

        self.assertFalse(
            validate_inputs(data)
        )

    def test_invalid_memory(self):
        data = self.valid()
        data["memory_load"] = -1

        self.assertFalse(
            validate_inputs(data)
        )

    def test_invalid_processes(self):
        data = self.valid()
        data["num_processes"] = -1

        self.assertFalse(
            validate_inputs(data)
        )

    def test_invalid_threads(self):
        data = self.valid()
        data["num_threads"] = -1

        self.assertFalse(
            validate_inputs(data)
        )

    def test_missing_input(self):
        data = self.valid()
        del data["ipc_intensity"]

        self.assertFalse(
            validate_inputs(data)
        )


if __name__ == "__main__":
    unittest.main()
