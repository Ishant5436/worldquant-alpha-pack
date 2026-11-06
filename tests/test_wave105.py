#!/usr/bin/env python3
"""
Unit and Quality Gate Invariant Tests for Wave 105 Grandmaster Expansion.
Deterministic Safety Standards: Functions <= 60 lines, assertion density >= 2.
"""
import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dispatch_wave105_grandmaster_expansion import build_wave105_candidates
from evaluate_wave105 import evaluate_quality_gates

def test_wave105_candidate_specifications():
    """Verify that Wave 105 defines exactly 5 orthogonal candidate architectures."""
    candidates = build_wave105_candidates()
    assert len(candidates) == 5, f"Expected 5 candidates, found {len(candidates)}"
    for cand in candidates:
        assert "name" in cand, "Candidate missing name"
        assert "expression" in cand, "Candidate missing expression"
        assert "universe" in cand, "Candidate missing universe"
        assert cand["universe"] in ["TOP200", "TOP500", "TOP1000"]
        assert "decay" in cand, "Candidate missing decay"
        assert cand["decay"] in [4, 5, 6]

def test_evaluate_quality_gates_pass():
    """Verify quality gate evaluation accepts institutional alpha metrics."""
    mock_alpha = {
        "is": {
            "sharpe": 1.55,
            "fitness": 1.25,
            "turnover": 0.14,
            "margin": 0.00135,
            "pnl": 4200000,
            "returns": 0.085,
            "drawdown": 0.065,
            "checks": [
                {"name": "LOW_SUB_UNIVERSE_SHARPE", "result": "PASS"}
            ]
        }
    }
    result = evaluate_quality_gates(mock_alpha)
    assert result["passes_is_gates"] is True, "Expected candidate to pass IS gates"
    assert result["sharpe"] == 1.55
    assert result["fitness"] == 1.25
    assert result["margin_bps"] == 13.5
    assert result["sub_universe_sharpe"] == "PASS"

def test_evaluate_quality_gates_fail_low_sharpe():
    """Verify quality gate evaluation rejects candidates failing Sharpe threshold."""
    mock_alpha = {
        "is": {
            "sharpe": 1.10,
            "fitness": 0.95,
            "turnover": 0.12,
            "margin": 0.00110,
            "pnl": 2000000,
            "returns": 0.04,
            "drawdown": 0.08,
            "checks": []
        }
    }
    result = evaluate_quality_gates(mock_alpha)
    assert result["passes_is_gates"] is False, "Expected candidate to fail IS gates"
    assert result["sharpe"] < 1.25
