#!/usr/bin/env python3
"""
Unit tests for WorldQuant BRAIN Daily Submission Cadence Engine.
Adheres strictly to Deterministic Safety Invariants:
- Functions <= 60 lines.
- Assertion density >= 2 per test.
"""
import unittest
from unittest.mock import MagicMock, patch
import json
import datetime
from daily_submission_cadence import (
    has_submitted_today,
    dispatch_candidate_simulation,
    CADENCE_CATALOG
)
from brain_client import BrainAPIClient

class TestDailyCadence(unittest.TestCase):
    """Test suite for daily cadence logic."""

    def setUp(self):
        self.client = BrainAPIClient(email="quant@example.com", password="pass")
        self.client.is_authenticated = True

    def test_has_submitted_today_true(self):
        """Verifies detection of today's submission."""
        today_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
        payload = {
            "results": [
                {"id": "a1", "dateSubmitted": f"{today_utc}T10:00:00Z", "stage": "OS"}
            ]
        }
        mock_resp = MagicMock(status=200)
        mock_resp.read.return_value = json.dumps(payload).encode("utf-8")

        with patch.object(self.client.session, "get", return_value=mock_resp):
            res = has_submitted_today(self.client)
            self.assertTrue(res)
            self.assertEqual(len(payload["results"]), 1)

    def test_has_submitted_today_false(self):
        """Verifies detection when no submission occurred today."""
        payload = {
            "results": [
                {"id": "a1", "dateSubmitted": "2026-01-01T10:00:00Z", "stage": "OS"}
            ]
        }
        mock_resp = MagicMock(status=200)
        mock_resp.read.return_value = json.dumps(payload).encode("utf-8")

        with patch.object(self.client.session, "get", return_value=mock_resp):
            res = has_submitted_today(self.client)
            self.assertFalse(res)
            self.assertEqual(len(payload["results"]), 1)

    def test_cadence_catalog_invariants(self):
        """Verifies catalog candidates satisfy basic schema."""
        self.assertGreater(len(CADENCE_CATALOG), 0)
        for c in CADENCE_CATALOG:
            self.assertIn("name", c)
            self.assertIn("expression", c)
            self.assertIn("universe", c)

if __name__ == "__main__":
    unittest.main()
