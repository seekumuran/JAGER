import unittest

from .import_audit import (
    ImportAudit,
)


class TestImportAudit(
    unittest.TestCase
):

    def test_valid_module(self):

        audit = ImportAudit(
            [
                "json",
                "pathlib",
            ]
        )

        self.assertTrue(
            audit.passed()
        )

    def test_invalid_module(self):

        audit = ImportAudit(
            [
                "json",
                "module_that_does_not_exist",
            ]
        )

        self.assertFalse(
            audit.passed()
        )

        summary = (
            audit.summary()
        )

        self.assertEqual(
            summary["total"],
            2,
        )

        self.assertEqual(
            summary["failed"],
            1,
        )


if __name__ == "__main__":
    unittest.main()
