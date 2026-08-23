import tempfile
import unittest

from .main import (
    build_parser,
    main,
)


class TestCLI(
    unittest.TestCase
):

    def test_parser(self):

        parser = build_parser()

        args = parser.parse_args(
            [
                "run",
                "mock",
                "Explore behavior",
            ]
        )

        self.assertEqual(
            args.command,
            "run",
        )

        self.assertEqual(
            args.target,
            "mock",
        )

    def test_help(self):

        result = main([])

        self.assertEqual(
            result,
            0,
        )

    def test_targets(self):

        result = main(
            ["targets"]
        )

        self.assertEqual(
            result,
            0,
        )

    def test_status(self):

        with tempfile.TemporaryDirectory() as tmp:

            result = main(
                [
                    "--state",
                    f"{tmp}/state.json",
                    "status",
                ]
            )

            self.assertEqual(
                result,
                0,
            )


if __name__ == "__main__":
    unittest.main()
