import unittest

from .target_adapter import (
    CallableTargetAdapter,
)


class TestTargetAdapter(unittest.TestCase):

    def test_callable_adapter(self):
        def target(**inputs):
            return {
                "status": "NORMAL",
                "inputs": inputs,
            }

        adapter = CallableTargetAdapter(target)

        result = adapter.observe(
            cpu_load=50,
        )

        self.assertEqual(
            result["status"],
            "NORMAL",
        )

        self.assertEqual(
            result["inputs"]["cpu_load"],
            50,
        )


if __name__ == "__main__":
    unittest.main()
