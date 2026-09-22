#!/usr/bin/env python3
"""
WorldQuant BRAIN Alpha Expression Validator
Enforces syntax validity, operator allowlist, and simulation settings integrity.
Follows Holzmann Power of 10 Deterministic Safety Invariants.
"""

import os
import re
from typing import Dict, List, Tuple, Any

# Canonical WorldQuant BRAIN grammar elements
ALLOWED_OPERATORS = {
    "rank", "ts_rank", "ts_mean", "ts_stddev", "stddev", "ts_decay_linear",
    "ts_delay", "ts_corr", "delta", "ts_max", "ts_min", "group_rank",
    "group_neutralize", "scale", "abs", "log", "sign", "power"
}

ALLOWED_FIELDS = {
    "close", "open", "high", "low", "volume", "vwap", "returns",
    "adv20", "subindustry", "industry", "sector", "market"
}


def _extract_settings_from_lines(lines: List[str]) -> Dict[str, str]:
    """Extracts simulation key-value settings from markdown list lines."""
    assert isinstance(lines, list), "lines parameter must be a list"
    assert len(lines) >= 0, "lines list must be non-negative length"

    settings: Dict[str, str] = {}
    for line in lines:
        match = re.search(r"-\s*([A-Za-z]+):\s*`?([^`\n]+)`?", line)
        if match:
            settings[match.group(1).strip()] = match.group(2).strip()
    return settings


def parse_alphas_from_readme(readme_path: str) -> List[Dict[str, Any]]:
    """Parses markdown file to extract all alpha definitions, expressions, and settings."""
    assert os.path.exists(readme_path), f"File not found: {readme_path}"
    assert os.path.isfile(readme_path), f"Path is not a regular file: {readme_path}"

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    alphas: List[Dict[str, Any]] = []
    sections = re.split(r"\n## Alpha\s+(\d+):\s*([^\n]+)", content)

    # First chunk is header, subsequent chunks come in triplets: (number, title, body)
    for i in range(1, len(sections), 3):
        alpha_num = int(sections[i])
        alpha_title = sections[i + 1].strip()
        body = sections[i + 2]

        expr_match = re.search(r"```text\s*\n(.*?)\n```", body, re.DOTALL)
        if not expr_match:
            continue
        expression = expr_match.group(1).strip()

        settings_lines = [l for l in body.split("\n") if l.strip().startswith("- ")]
        settings = _extract_settings_from_lines(settings_lines)

        alphas.append({
            "number": alpha_num,
            "name": f"Alpha {alpha_num}: {alpha_title}",
            "expression": expression,
            "settings": settings,
        })

    assert len(alphas) > 0, "No alpha expressions could be extracted from README"
    return alphas


def validate_alpha_expression(expression: str) -> Tuple[bool, List[str]]:
    """Validates mathematical expression syntax, parentheses, and identifier grammar."""
    assert isinstance(expression, str), "expression must be a string"
    assert len(expression.strip()) > 0, "expression cannot be empty"

    errors: List[str] = []

    # 1. Balanced parentheses
    if expression.count("(") != expression.count(")"):
        errors.append(f"Unbalanced parentheses: '('={expression.count('(')}, ')'={expression.count(')')}")

    # 2. Extract identifiers (words)
    tokens = re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", expression)
    for token in tokens:
        if token not in ALLOWED_OPERATORS and token not in ALLOWED_FIELDS:
            errors.append(f"Unknown or unauthorized identifier: '{token}'")

    is_valid = len(errors) == 0
    return is_valid, errors
