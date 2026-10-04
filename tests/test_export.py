"""
Tests for WorldQuant BRAIN Alpha Exporter.
Deterministic Safety Standards: Functions <= 60 lines, assertion density >= 2.
"""
import os
import csv
import pytest
from export_batch import export_batch_artifacts


def test_export_batch_artifacts(tmp_path):
    """Tests generation of CSV and web text files for bulk upload."""
    sample_alphas = [
        {
            "number": 1,
            "name": "Alpha 1: Volatility Mean Reversion",
            "expression": "-1 * rank(delta(close, 5))",
            "settings": {
                "Region": "USA",
                "Universe": "TOP3000",
                "Neutralization": "Subindustry",
                "Truncation": "0.08"
            }
        },
        {
            "number": 2,
            "name": "Alpha 2: Volume Range Reversion",
            "expression": "-1 * rank(ts_rank(close, 10))",
            "settings": {
                "Region": "USA",
                "Universe": "TOP3000",
                "Neutralization": "Subindustry",
                "Truncation": "0.08"
            }
        }
    ]
    csv_file = str(tmp_path / "alphas.csv")
    txt_file = str(tmp_path / "alphas.txt")

    count = export_batch_artifacts(sample_alphas, csv_file, txt_file)
    assert count == 2, "Exported count must match input count"
    assert os.path.exists(csv_file), "CSV file was not created"
    assert os.path.exists(txt_file), "TXT file was not created"

    with open(csv_file, "r") as f:
        reader = list(csv.DictReader(f))
        assert len(reader) == 2, "CSV must contain 2 rows"
        assert "expression" in reader[0], "CSV must include expression header"

    with open(txt_file, "r") as f:
        content = f.read()
        assert "Alpha 1:" in content, "TXT must include Alpha 1 header"
        assert "Alpha 2:" in content, "TXT must include Alpha 2 header"
