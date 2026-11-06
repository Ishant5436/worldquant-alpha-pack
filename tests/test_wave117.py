"""
Unit and Regression Tests for Wave 117 Orthogonal Expansion Alpha #103.
Deterministic Safety Standards: Functions <= 60 lines, assertion density >= 2.
"""
import json
import os
import pytest
from dispatch_wave117_orthogonal_expansion import build_wave117_candidates
from evaluate_wave117 import evaluate_quality_gates

def test_build_wave117_candidates_spec():
    """Verify Wave 117 specifications are structurally valid."""
    cands = build_wave117_candidates()
    assert len(cands) == 5, "Must contain exactly 5 candidates"
    for c in cands:
        assert "name" in c and len(c["name"]) > 0
        assert "expression" in c and len(c["expression"]) > 0
        assert c["universe"] == "TOP1000"
        assert c["decay"] == 5

def test_evaluate_quality_gates_103_pass():
    """Verify Alpha #103 passes all 7 Quality Gates with compliant metrics."""
    mock_alpha_103 = {
        "is": {
            "sharpe": 1.65,
            "fitness": 1.38,
            "turnover": 0.1186,
            "margin": 0.001469,
            "pnl": 4311162,
            "returns": 0.082,
            "drawdown": 0.051,
            "checks": [
                {"name": "LOW_SHARPE", "result": "PASS", "limit": 1.25, "value": 1.65},
                {"name": "LOW_FITNESS", "result": "PASS", "limit": 1.00, "value": 1.38},
                {"name": "LOW_TURNOVER", "result": "PASS", "limit": 0.01, "value": 0.1186},
                {"name": "HIGH_TURNOVER", "result": "PASS", "limit": 0.70, "value": 0.1186},
                {"name": "CONCENTRATED_WEIGHT", "result": "PASS"},
                {"name": "LOW_SUB_UNIVERSE_SHARPE", "result": "PASS", "limit": 1.10, "value": 1.23},
                {"name": "SELF_CORRELATION", "result": "PASS", "limit": 0.70, "value": 0.612}
            ]
        }
    }
    res = evaluate_quality_gates(mock_alpha_103)
    assert res["passes_is_gates"] is True, "Alpha #103 must pass all IS quality gates"
    assert res["sharpe"] == 1.65, "Sharpe must match"
    assert res["fitness"] == 1.38, "Fitness must match"
    assert res["sub_universe_sharpe"] == "PASS", "Sub-universe check must be PASS"

def test_alpha_103_admitted_in_fleet():
    """Verify Alpha #103 is recorded in submitted_alphas.json in active OS state."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "submitted_alphas.json")
    with open(path) as f:
        data = json.load(f)
    assert data["submitted_count"] == 103
    alpha_103 = next((a for a in data["alphas"] if a["id"] == "P0ozdMwx"), None)
    assert alpha_103 is not None, "Alpha P0ozdMwx not found in fleet"
    assert alpha_103["stage"] == "OS"
    assert alpha_103["status"] == "ACTIVE"
    assert alpha_103["metrics"]["sharpe"] >= 1.60
    assert alpha_103["metrics"]["fitness"] >= 1.30
