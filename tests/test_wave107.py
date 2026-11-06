#!/usr/bin/env python3
"""
Unit and Quality Gate Invariant Tests for Wave 107 Spectacular Alpha Sprint.
Deterministic Safety Standards: Functions <= 60 lines, assertion density >= 2.
"""
import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dispatch_wave107_spectacular_roe import build_wave107_candidates
from evaluate_wave107 import evaluate_quality_gates

def test_wave107_candidate_specifications():
    """Verify that Wave 107 defines exactly 5 orthogonal candidate architectures."""
    candidates = build_wave107_candidates()
    assert len(candidates) == 5, f"Expected 5 candidates, found {len(candidates)}"
    for cand in candidates:
        assert "name" in cand, "Candidate missing name"
        assert "expression" in cand, "Candidate missing expression"
        assert "universe" in cand, "Candidate missing universe"
        assert cand["universe"] in ["TOP500", "TOP1000"]
        assert "decay" in cand, "Candidate missing decay"
        assert cand["decay"] in [4, 5, 6]

def test_evaluate_quality_gates_roe_pass():
    """Verify quality gate evaluation accepts spectacular ROE alpha metrics."""
    mock_alpha = {
        "is": {
            "sharpe": 1.95,
            "fitness": 1.55,
            "turnover": 0.13,
            "margin": 0.00130,
            "pnl": 4500000,
            "returns": 0.080,
            "drawdown": 0.045,
            "checks": [
                {"name": "LOW_SUB_UNIVERSE_SHARPE", "result": "PASS"}
            ]
        }
    }
    result = evaluate_quality_gates(mock_alpha)
    assert result["passes_is_gates"] is True, "Expected candidate to pass IS gates"
    assert result["sharpe"] == 1.95
    assert result["fitness"] == 1.55
    assert result["margin_bps"] == 13.0
    assert result["sub_universe_sharpe"] == "PASS"

def test_evaluate_quality_gates_rejects_low_fitness():
    """Verify quality gate evaluation rejects candidates failing fitness threshold."""
    mock_alpha = {
        "is": {
            "sharpe": 1.35,
            "fitness": 0.85,
            "turnover": 0.12,
            "margin": 0.00115,
            "pnl": 2800000,
            "returns": 0.05,
            "drawdown": 0.07,
            "checks": [
                {"name": "LOW_SUB_UNIVERSE_SHARPE", "result": "PASS"}
            ]
        }
    }
    result = evaluate_quality_gates(mock_alpha)
    assert result["passes_is_gates"] is False, "Expected candidate to fail IS gates"
    assert result["fitness"] < 1.00
