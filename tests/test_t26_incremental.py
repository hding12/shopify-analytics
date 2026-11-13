"""Regression tests for the T26 historical knowledge bundle. No external API use."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import validate_incremental_records as audit


class T26AuditTests(unittest.TestCase):
    def test_public_addendum_validates(self):
        self.assertIn("PASS:", audit.validate())

    def test_bearer_and_email_must_be_excluded_from_public_repo(self):
        self.assertFalse(audit.safe_public_text("user@example.com"))
        self.assertFalse(audit.safe_public_text("Bearer " + "abcd" * 8))
        self.assertFalse(audit.safe_public_text("shpat_" + "A" * 26))

    def test_scope_and_safe_labels(self):
        self.assertTrue(audit.safe_public_text("campaign 24447529143, two RSA IDs, 120 CNY/day"))
        self.assertFalse(audit.aware(None))
        self.assertFalse(audit.aware("2026-11-13T00:00:00"))
        self.assertTrue(audit.aware("2026-11-13T01:18:39Z"))


if __name__ == "__main__":
    unittest.main()
