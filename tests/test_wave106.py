#!/usr/bin/env python3
"""
Unit and Quality Gate Invariant Tests for Wave 106 Spectacular Alpha Sprint.
Deterministic Safety Standards: Functions <= 60 lines, assertion density >= 2.
"""
import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dispatch_wave106_spectacular_alpha import build_wave106_candidates
from evaluate_wave106 import evaluate_quality_gates

def test_wave106_candidate_specifications():
    """Verify that Wave 106 defines exactly 5 orthogonal candidate architectures."""
    candidates = build_wave106_candidates()
    assert len(candidates) == 5, f"Expected 5 candidates, found {len(candidates)}"
    for cand in candidates:
        assert "name" in cand, "Candidate missing name"
        assert "expression" in cand, "Candidate missing expression"
        assert "universe" in cand, "Candidate missing universe"
        assert cand["universe"] in ["TOP500", "TOP1000"]
        assert "decay" in cand, "Candidate missing decay"
        assert cand["decay"] in [4, 5, 6]

def test_evaluate_quality_gates_spectacular_pass():
    """Verify quality gate evaluation accepts spectacular alpha metrics."""
    mock_alpha = {
        "is": {
            "sharpe": 2.25,
            "fitness": 1.75,
            "turnover": 0.14,
            "margin": 0.00155,
            "pnl": 5800000,
            "returns": 0.095,
            "drawdown": 0.045,
            "checks": [
                {"name": "LOW_SUB_UNIVERSE_SHARPE", "result": "PASS"}
            ]
        }
    }
    result = evaluate_quality_gates(mock_alpha)
    assert result["passes_is_gates"] is True, "Expected candidate to pass IS gates"
    assert result["sharpe"] == 2.25
    assert result["fitness"] == 1.75
    assert result["margin_bps"] == 15.5
    assert result["sub_universe_sharpe"] == "PASS"

def test_evaluate_quality_gates_rejects_sub_universe_fail():
    """Verify quality gate evaluation rejects candidates failing sub-universe Sharpe."""
    mock_alpha = {
        "is": {
            "sharpe": 1.80,
            "fitness": 1.40,
            "turnover": 0.15,
            "margin": 0.00120,
            "pnl": 3500000,
            "returns": 0.06,
            "drawdown": 0.07,
            "checks": [
                {"name": "LOW_SUB_UNIVERSE_SHARPE", "result": "FAIL"}
            ]
        }
    }
    result = evaluate_quality_gates(mock_alpha)
    assert result["passes_is_gates"] is False, "Expected candidate to fail IS gates"
    assert result["sub_universe_sharpe"] == "FAIL"
