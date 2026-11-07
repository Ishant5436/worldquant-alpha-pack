"""
Unit and Regression Tests for Wave 121 Milestone Alpha #104.
Deterministic Safety Standards: Functions <= 60 lines, assertion density >= 2.
"""
import json
import os
import pytest
from dispatch_wave121_half_billion_unlock import build_wave121_candidates
from evaluate_wave121 import evaluate_quality_gates

def test_build_wave121_candidates_spec():
    """Verify Wave 121 specifications are structurally valid."""
    cands = build_wave121_candidates()
    assert len(cands) == 4, "Must contain exactly 4 candidates"
    for c in cands:
        assert "name" in c and len(c["name"]) > 0
        assert "expression" in c and len(c["expression"]) > 0
        assert c["universe"] in ["TOP1000", "TOP500"]
        assert c["decay"] in [5, 6]

def test_evaluate_quality_gates_104_pass():
    """Verify Alpha #104 passes all 7 Quality Gates with compliant metrics."""
    mock_alpha_104 = {
        "is": {
            "sharpe": 2.17,
            "fitness": 1.89,
            "turnover": 0.1235,
            "margin": 0.001535,
            "pnl": 4692059,
            "returns": 0.0945,
            "drawdown": 0.0435,
            "checks": [
                {"name": "LOW_SHARPE", "result": "PASS", "limit": 1.25, "value": 2.17},
                {"name": "LOW_FITNESS", "result": "PASS", "limit": 1.00, "value": 1.89},
                {"name": "LOW_TURNOVER", "result": "PASS", "limit": 0.01, "value": 0.1235},
                {"name": "HIGH_TURNOVER", "result": "PASS", "limit": 0.70, "value": 0.1235},
                {"name": "CONCENTRATED_WEIGHT", "result": "PASS"},
                {"name": "LOW_SUB_UNIVERSE_SHARPE", "result": "PASS", "limit": 1.15, "value": 1.45},
                {"name": "SELF_CORRELATION", "result": "PASS", "limit": 0.70, "value": 0.691}
            ]
        }
    }
    res = evaluate_quality_gates(mock_alpha_104)
    assert res["passes_is_gates"] is True, "Alpha #104 must pass all IS quality gates"
    assert res["sharpe"] == 2.17, "Sharpe must match"
    assert res["fitness"] == 1.89, "Fitness must match"
    assert res["sub_universe_sharpe"] == "PASS", "Sub-universe check must be PASS"

def test_alpha_104_admitted_in_fleet():
    """Verify Alpha #104 is recorded in submitted_alphas.json in active OS state."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "submitted_alphas.json")
    with open(path) as f:
        data = json.load(f)
    assert data["submitted_count"] >= 104
    alpha_104 = next((a for a in data["alphas"] if a["id"] == "9qxMoq82"), None)
    assert alpha_104 is not None, "Alpha 9qxMoq82 not found in fleet"
    assert alpha_104["stage"] == "OS"
    assert alpha_104["status"] == "ACTIVE"
    assert alpha_104["metrics"]["sharpe"] >= 2.0
    assert alpha_104["metrics"]["fitness"] >= 1.8
    assert data["portfolio_summary"]["cumulative_is_pnl"] >= 500_000_000
