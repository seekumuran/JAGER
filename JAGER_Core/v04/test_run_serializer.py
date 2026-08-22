import unittest
from dataclasses import dataclass

from .run_serializer import serialize


@dataclass
class Sample:
    name: str
    value: int


class TestRunSerializer(unittest.TestCase):

    def test_dataclass(self):

        result = serialize(
            Sample(
                name="test",
                value=42,
            )
        )

        self.assertEqual(
            result,
            {
                "name": "test",
                "value": 42,
            },
        )

    def test_nested_structure(self):

        result = serialize(
            {
                "items": [
                    Sample(
                        name="a",
                        value=1,
                    ),
                    Sample(
                        name="b",
                        value=2,
                    ),
                ]
            }
        )

        self.assertEqual(
            result["items"][0]["name"],
            "a",
        )

        self.assertEqual(
            result["items"][1]["value"],
            2,
        )


if __name__ == "__main__":
    unittest.main()
