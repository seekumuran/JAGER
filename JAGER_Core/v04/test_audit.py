import unittest

from .audit import AuditTrail


class TestAuditTrail(unittest.TestCase):

    def test_valid_audit(self):
        audit = AuditTrail()

        audit.append(
            "ACTION",
            {"value": 42},
        )

        self.assertTrue(
            audit.verify()
        )

    def test_tampering_detected(self):
        audit = AuditTrail()

        audit.append(
            "ACTION",
            {"value": 42},
        )

        audit.records[0]["payload"]["value"] = 99

        self.assertFalse(
            audit.verify()
        )


if __name__ == "__main__":
    unittest.main()
