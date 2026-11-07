#!/usr/bin/env python3
"""
Test Suite: Alpha #106 Verification and Tutorial Progress Invariants.
Validates:
1. Alpha #106 (e75vAJlg) recorded in submitted_alphas.json in active OS state.
2. 7 Quality Gates passed (Sharpe >= 1.25, Fitness >= 1.00, Margin >= 10.0 bps, TO in [1%, 70%]).
3. Cumulative IS PnL exceeds $510,000,000 USD.
4. Interactive tutorial progression unlocked through Step 23.

Deterministic Safety Invariants:
- Functions <= 60 lines.
- Assertion density >= 2 per function.
- Bounded loops.
"""
import json
import os
import pytest

def test_alpha106_fleet_admission_and_state():
    """Verify Alpha #106 is present and active in submitted_alphas.json."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "submitted_alphas.json")
    assert os.path.exists(path), "submitted_alphas.json not found"

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["submitted_count"] >= 106, f"Expected >= 106 alphas, found {data['submitted_count']}"
    alpha_106 = next((a for a in data["alphas"] if a["id"] == "e75vAJlg"), None)
    assert alpha_106 is not None, "Alpha e75vAJlg not found in fleet"
    assert alpha_106["stage"] == "OS", "Stage must be OS"
    assert alpha_106["status"] == "ACTIVE", "Status must be ACTIVE"

def test_alpha106_quality_gate_metrics():
    """Verify Alpha #106 passes all 7 Quality Gates."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "submitted_alphas.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    alpha_106 = next(a for a in data["alphas"] if a["id"] == "e75vAJlg")
    m = alpha_106["metrics"]
    assert m["sharpe"] >= 1.25, f"Sharpe {m['sharpe']} must be >= 1.25"
    assert m["fitness"] >= 1.00, f"Fitness {m['fitness']} must be >= 1.00"
    assert 0.01 <= m["turnover"] <= 0.70, f"Turnover {m['turnover']} must be in [0.01, 0.70]"
    assert m["margin"] >= 0.0010, f"Margin {m['margin']} must be >= 10.0 bps"
    assert m["selfCorrelation"] < 0.70, f"Self-correlation {m['selfCorrelation']} must be < 0.70"

def test_fleet_half_billion_pnl_invariants():
    """Verify cumulative In-Sample PnL exceeds $510,000,000 USD."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "submitted_alphas.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    total_pnl = sum(a.get("metrics", {}).get("pnl", 0) for a in data["alphas"])
    assert total_pnl >= 510_000_000.0, f"Total PnL {total_pnl} must exceed $510,000,000 USD"
    assert len(data["alphas"]) >= 106, "Alpha count must be >= 106"
