#!/usr/bin/env python3
"""
Unit and Regression Tests for Wave 116 Spectacular Alpha #102.
Deterministic Safety Standards: Functions <= 60 lines, assertion density >= 2.
"""
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from evaluate_wave116 import evaluate_quality_gates

def test_wave116_candidate_specifications():
    """Verify Wave 116 dispatch candidate count and syntax."""
    disp_path = os.path.join(os.path.dirname(__file__), "..", "wave116_dispatches.json")
    assert os.path.exists(disp_path), "wave116_dispatches.json must exist"
    with open(disp_path, "r", encoding="utf-8") as f:
        dispatches = json.load(f)
    assert len(dispatches) == 5, f"Expected 5 candidates, got {len(dispatches)}"
    for d in dispatches:
        assert "sim_id" in d and d["sim_id"] is not None
        assert "name" in d and len(d["name"]) > 0

def test_evaluate_quality_gates_spectacular_102_pass():
    """Verify Alpha #102 passes all 7 Quality Gates with stellar Sharpe and Fitness."""
    mock_alpha_102 = {
        "id": "qMLG80gZ",
        "is": {
            "sharpe": 2.08,
            "fitness": 1.90,
            "turnover": 0.1236,
            "margin": 0.001696,
            "pnl": 5183541,
            "returns": 0.1048,
            "drawdown": 0.0448,
            "checks": [
                {"name": "LOW_SHARPE", "result": "PASS"},
                {"name": "LOW_FITNESS", "result": "PASS"},
                {"name": "LOW_TURNOVER", "result": "PASS"},
                {"name": "HIGH_TURNOVER", "result": "PASS"},
                {"name": "CONCENTRATED_WEIGHT", "result": "PASS"},
                {"name": "LOW_SUB_UNIVERSE_SHARPE", "result": "PASS"}
            ]
        }
    }
    res = evaluate_quality_gates(mock_alpha_102)
    assert res["passes_is_gates"] is True, "Alpha #102 must pass all IS quality gates"
    assert res["sharpe"] == 2.08
    assert res["fitness"] == 1.90
    assert res["sub_universe_sharpe"] == "PASS"
    assert res["margin_bps"] >= 10.0

def test_alpha_102_admitted_in_fleet():
    """Verify Alpha #102 is recorded in submitted_alphas.json in active OS state."""
    sub_path = os.path.join(os.path.dirname(__file__), "..", "submitted_alphas.json")
    assert os.path.exists(sub_path), "submitted_alphas.json must exist"
    with open(sub_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["submitted_count"] == 102
    alpha_102 = next((a for a in data["alphas"] if a["id"] == "qMLG80gZ"), None)
    assert alpha_102 is not None, "Alpha qMLG80gZ not found in fleet"
    assert alpha_102["stage"] == "OS"
    assert alpha_102["status"] == "ACTIVE"
    assert alpha_102["metrics"]["sharpe"] >= 2.00
    assert alpha_102["metrics"]["fitness"] >= 1.80
