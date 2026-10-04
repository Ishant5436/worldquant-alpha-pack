#!/usr/bin/env python3
"""
WorldQuant BRAIN Alpha Batch Exporter.
Deterministic Safety Standards: Functions <= 60 lines, assertion density >= 2.
"""
import csv
import json
import os
import sys
from typing import List, Dict, Any


def export_batch_artifacts(
    alphas: List[Dict[str, Any]],
    csv_path: str,
    txt_path: str
) -> int:
    """Exports structured alpha expressions to CSV and human-readable text."""
    assert isinstance(alphas, list), "Alphas must be a list"
    assert len(alphas) > 0, "Alphas list must not be empty"
    assert isinstance(csv_path, str) and len(csv_path) > 0, "Invalid CSV path"
    assert isinstance(txt_path, str) and len(txt_path) > 0, "Invalid TXT path"

    fieldnames = ["alpha_id", "name", "expression", "region", "universe", "neutralization", "truncation"]
    rows = []
    text_blocks = []

    for item in alphas:
        settings = item.get("settings", {})
        row = {
            "alpha_id": item.get("number", 0),
            "name": item.get("name", "Unnamed"),
            "expression": item.get("expression", ""),
            "region": settings.get("Region", "USA"),
            "universe": settings.get("Universe", "TOP3000"),
            "neutralization": settings.get("Neutralization", "Subindustry"),
            "truncation": settings.get("Truncation", "0.08"),
        }
        rows.append(row)

        block = (
            f"=== {row['name']} ===\n"
            f"Expression:     {row['expression']}\n"
            f"Region:         {row['region']}\n"
            f"Universe:       {row['universe']}\n"
            f"Neutralization: {row['neutralization']}\n"
            f"Truncation:     {row['truncation']}\n"
            "------------------------------------------------------------\n"
        )
        text_blocks.append(block)

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.writelines(text_blocks)

    assert os.path.exists(csv_path), "CSV export file missing"
    assert os.path.exists(txt_path), "TXT export file missing"
    return len(rows)


def load_and_export(
    source_json: str = "qualifying_alphas.json",
    csv_out: str = "batch_submission_table.csv",
    txt_out: str = "batch_submission_web.txt"
) -> int:
    """Loads validated alphas and generates portal-ready artifacts."""
    assert os.path.exists(source_json), f"Source file {source_json} does not exist"
    with open(source_json, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert "alphas" in data, "Malformed alpha vault json"

    count = export_batch_artifacts(data["alphas"], csv_out, txt_out)
    assert count == len(data["alphas"]), "Export count mismatch"
    print(f"[OK] Exported {count} alphas to '{csv_out}' and '{txt_out}'.")
    return count


if __name__ == "__main__":
    src = "qualifying_alphas.json" if len(sys.argv) < 2 else sys.argv[1]
    load_and_export(source_json=src)
