#!/usr/bin/env python3
"""
Unit and Invariant Tests for WorldQuant BRAIN Alpha Pack
Validates syntax, operator signatures, balanced parentheses, and portfolio diversity.
"""

import os
import re
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from validator import parse_alphas_from_readme, validate_alpha_expression, ALLOWED_OPERATORS, ALLOWED_FIELDS

README_PATH = os.path.join(os.path.dirname(__file__), "..", "README.md")


def test_readme_contains_minimum_twelve_alphas():
    """Verify that the alpha pack contains at least 12 distinct alphas."""
    alphas = parse_alphas_from_readme(README_PATH)
    assert len(alphas) >= 12, f"Expected at least 12 alphas, found {len(alphas)}"
    assert isinstance(alphas, list), "Alphas must be returned as a list"


def test_all_alphas_have_balanced_parentheses():
    """Verify that every alpha formula has perfectly balanced parentheses."""
    alphas = parse_alphas_from_readme(README_PATH)
    assert len(alphas) >= 1, "Must have at least one alpha to validate"
    for item in alphas:
        expr = item["expression"]
        open_count = expr.count("(")
        close_count = expr.count(")")
        assert open_count == close_count, f"Unbalanced parentheses in {item['name']}: {open_count} vs {close_count}"


def test_all_alpha_expressions_use_valid_grammar():
    """Verify that all tokens in each alpha formula conform to WorldQuant BRAIN grammar."""
    alphas = parse_alphas_from_readme(README_PATH)
    assert len(alphas) >= 1, "Must have at least one alpha to validate"
    for item in alphas:
        is_valid, errors = validate_alpha_expression(item["expression"])
        assert is_valid, f"Alpha {item['name']} failed validation: {errors}"


def test_all_alphas_have_required_simulation_settings():
    """Verify that every alpha includes Region, Universe, Neutralization, and Truncation."""
    alphas = parse_alphas_from_readme(README_PATH)
    assert len(alphas) >= 1, "Must have at least one alpha to validate"
    for item in alphas:
        settings = item.get("settings", {})
        assert "Region" in settings, f"Missing Region in {item['name']}"
        assert settings["Region"] == "USA", f"Invalid Region in {item['name']}: {settings['Region']}"
        assert "Universe" in settings, f"Missing Universe in {item['name']}"
        assert settings["Universe"] in ["TOP3000", "TOP2000", "TOP1000"], f"Invalid Universe in {item['name']}"
        assert "Neutralization" in settings, f"Missing Neutralization in {item['name']}"
