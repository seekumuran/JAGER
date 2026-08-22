import unittest

from .validation import validate_inputs
from .errors import InvalidActionError


class TestErrors(unittest.TestCase):

    def test_missing_inputs_raise_error(self):
        with self.assertRaises(
            InvalidActionError
        ):
            validate_inputs({})

    def test_invalid_cpu_raises_error(self):
        data = {
            "cpu_load": 101,
            "memory_load": 50,
            "num_processes": 10,
            "num_threads": 10,
            "ipc_intensity": 50,
        }

        with self.assertRaises(
            InvalidActionError
        ):
            validate_inputs(data)


if __name__ == "__main__":
    unittest.main()
