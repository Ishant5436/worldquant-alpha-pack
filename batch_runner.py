#!/usr/bin/env python3
"""
Batch Simulation Runner for WorldQuant BRAIN Alpha Pack.
Deterministic Safety Standards: Functions <= 60 lines, assertion density >= 2.
"""
import argparse
import json
import os
import sys
from typing import List, Dict, Any

from validator import parse_alphas_from_readme, validate_alpha_expression
from brain_client import BrainAPIClient

README_PATH = os.path.join(os.path.dirname(__file__), "README.md")
OUTPUT_MANIFEST = os.path.join(os.path.dirname(__file__), "qualifying_alphas.json")


def load_and_validate_alphas(readme_path: str) -> List[Dict[str, Any]]:
    """Loads all alpha definitions from README and validates expression syntax."""
    assert os.path.exists(readme_path), f"README not found: {readme_path}"
    alphas = parse_alphas_from_readme(readme_path)
    assert len(alphas) >= 20, f"Insufficient alpha count: {len(alphas)}"

    validated = []
    for alpha in alphas:
        is_valid, errors = validate_alpha_expression(alpha["expression"])
        if is_valid:
            validated.append(alpha)
        else:
            print(f"[WARN] Skipping invalid alpha {alpha['name']}: {errors}")
    return validated


def run_batch_simulation(alphas: List[Dict[str, Any]], dry_run: bool = False) -> Dict[str, Any]:
    """Runs batch simulation lifecycle or dry-run validation manifest."""
    assert isinstance(alphas, list), "Alphas must be a list"
    assert len(alphas) > 0, "Alphas list cannot be empty"

    client = BrainAPIClient()
    results = []

    if dry_run or not client.is_configured:
        print("[INFO] Executing in DRY-RUN validation mode (No live credentials or --dry-run set).")
        for a in alphas:
            results.append({
                "number": a["number"],
                "name": a["name"],
                "status": "VALIDATED_LOCAL",
                "expression": a["expression"],
                "settings": a["settings"],
            })
        return {"mode": "DRY_RUN", "total": len(alphas), "qualifying": len(results), "alphas": results}

    if not client.authenticate():
        print("[ERROR] BRAIN API authentication failed. Check credentials.")
        return {"mode": "ERROR", "error": "Authentication failed", "alphas": []}

    print(f"[INFO] Authenticated. Dispatching simulations for {len(alphas)} alphas...")
    for a in alphas:
        sim_id = client.dispatch_simulation(a)
        if sim_id:
            res = client.poll_simulation(sim_id)
            is_qualifying = res.get("sharpe", 0.0) >= 1.25 and res.get("turnover", 1.0) <= 0.70
            results.append({"name": a["name"], "metrics": res, "qualifying": is_qualifying})

    return {"mode": "LIVE", "total": len(alphas), "alphas": results}


def save_manifest(manifest: Dict[str, Any], output_path: str):
    """Saves simulation and audit manifest to JSON file."""
    assert isinstance(manifest, dict), "Manifest must be a dictionary"
    assert isinstance(output_path, str) and len(output_path) > 0, "Invalid output path"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"[INFO] Saved audit manifest to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WorldQuant BRAIN Batch Runner")
    parser.add_argument("--dry-run", action="store_true", default=False, help="Run local validation only")
    args = parser.parse_args()

    alpha_catalog = load_and_validate_alphas(README_PATH)
    batch_manifest = run_batch_simulation(alpha_catalog, dry_run=args.dry_run)
    save_manifest(batch_manifest, OUTPUT_MANIFEST)
