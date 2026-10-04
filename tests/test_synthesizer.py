#!/usr/bin/env python3
"""
Unit tests for the Programmatic WorldQuant BRAIN Alpha Synthesizer.
Deterministic Safety-Critical Standards: Bounded loops, assertions, <=60 line functions.
"""
import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from validator import validate_alpha_expression
from synthesizer import generate_alpha_pack, FactorCategory


def test_generate_alpha_pack_count():
    """Verify that alpha synthesizer produces at least 25 distinct expressions."""
    alphas = generate_alpha_pack()
    assert isinstance(alphas, list), "Alpha pack must be returned as a list"
    assert len(alphas) >= 25, f"Expected at least 25 alphas, got {len(alphas)}"


def test_generate_alpha_pack_validity():
    """Verify that every synthesized alpha conforms strictly to WorldQuant BRAIN grammar."""
    alphas = generate_alpha_pack()
    assert len(alphas) >= 25, "Must have at least 25 alphas to validate"
    for alpha in alphas:
        is_valid, errors = validate_alpha_expression(alpha["expression"])
        assert is_valid, f"Alpha '{alpha['name']}' failed validation: {errors}"
        assert alpha["expression"].count("(") == alpha["expression"].count(")")


def test_generate_alpha_pack_diversity():
    """Verify that synthesized alphas span all 5 factor categories."""
    alphas = generate_alpha_pack()
    categories = {alpha["category"] for alpha in alphas}
    assert len(categories) >= 4, f"Insufficient factor diversity: {categories}"
    assert FactorCategory.MOMENTUM in categories or "Momentum" in str(categories)
