#!/usr/bin/env python3
"""
WorldQuant BRAIN - Autonomous Daily Submission Cadence Engine.
Maintains continuous 'Days of Submission' momentum on Country Leaderboard.
Adheres strictly to Gerard Holzmann Power of 10 Deterministic Safety Invariants:
- Functions <= 60 lines.
- Assertion density >= 2 per function.
- Strict parameter bounds.
"""
import os
import sys
import time
import json
import datetime
from typing import Dict, Any, List, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brain_client import BrainAPIClient

def init_authenticated_client() -> BrainAPIClient:
    """Initializes and authenticates BRAIN client."""
    email = os.environ.get("BRAIN_EMAIL", "panchaleshant@gmail.com")
    password = os.environ.get("BRAIN_PASSWORD", "punpe7-bemfiw-gyjwyW")
    assert len(email) > 0, "Email parameter must not be empty"
    assert len(password) > 0, "Password parameter must not be empty"

    client = BrainAPIClient(email=email, password=password)
    assert client.authenticate(), "Authentication failed"
    return client

def has_submitted_today(client: BrainAPIClient) -> bool:
    """Checks if an alpha has already been submitted in the current UTC day."""
    assert client.is_authenticated, "Client unauthenticated"
    assert client.session is not None, "Session uninitialized"

    url = "https://api.worldquantbrain.com/users/self/alphas?stage=OS&limit=10"
    resp = client.session.get(url, timeout=15)
    assert resp.status == 200, f"HTTP Error {resp.status}"

    data = json.loads(resp.read().decode("utf-8"))
    results = data.get("results", [])
    today_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    for a in results:
        date_sub = a.get("dateSubmitted") or ""
        if date_sub.startswith(today_utc):
            return True
    return False

def dispatch_candidate_simulation(client: BrainAPIClient, spec: Dict[str, Any]) -> Optional[str]:
    """Dispatches simulation candidate and returns simulation ID."""
    assert client.is_authenticated, "Client unauthenticated"
    assert "expression" in spec and "universe" in spec, "Missing spec parameters"

    payload = {
        "name": spec.get("name", "DAILY_CADENCE_ALPHA"),
        "expression": spec["expression"],
        "settings": {
            "Universe": spec["universe"],
            "Decay": spec.get("decay", 5),
            "Neutralization": "SUBINDUSTRY",
            "Truncation": 0.08
        }
    }
    return client.dispatch_simulation(payload)

def poll_simulation_result(client: BrainAPIClient, sim_id: str, timeout: int = 180) -> Optional[str]:
    """Polls simulation until completion and returns alpha ID."""
    assert client.is_authenticated, "Client unauthenticated"
    assert len(sim_id) > 0, "Invalid simulation ID"

    url = f"https://api.worldquantbrain.com/simulations/{sim_id}"
    start = time.time()
    while time.time() - start < timeout:
        try:
            resp = client.session.get(url, timeout=10)
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                status = data.get("status")
                if status == "COMPLETED" or data.get("alpha"):
                    alpha = data.get("alpha")
                    return alpha.get("id") if isinstance(alpha, dict) else alpha
                elif status in ["ERROR", "FAILED"]:
                    return None
        except Exception:
            pass
        time.sleep(3)
    return None

def verify_and_submit_alpha(client: BrainAPIClient, alpha_id: str) -> Dict[str, Any]:
    """Evaluates alpha metrics and submits if quality gates pass."""
    assert client.is_authenticated, "Client unauthenticated"
    assert len(alpha_id) > 0, "Alpha ID must not be empty"

    url = f"https://api.worldquantbrain.com/alphas/{alpha_id}"
    resp = client.session.get(url, timeout=10)
    data = json.loads(resp.read().decode("utf-8"))
    m = data.get("is", {})
    sharpe = float(m.get("sharpe", 0.0))
    fitness = float(m.get("fitness", 0.0))
    turnover = float(m.get("turnover", 0.0))

    if not (sharpe >= 1.25 and fitness >= 1.0 and 0.01 <= turnover <= 0.70):
        return {"admitted": False, "reason": "QUALITY_GATES_FAILED"}

    sub_url = f"https://api.worldquantbrain.com/alphas/{alpha_id}/submit"
    try:
        sub_resp = client.session.post(sub_url, timeout=15)
        assert sub_resp.status in [200, 201], f"Submit failed: {sub_resp.status}"
    except Exception as e:
        return {"admitted": False, "error": str(e)}

    for _ in range(12):
        time.sleep(5)
        try:
            r = client.session.get(url, timeout=10)
            rec = json.loads(r.read().decode("utf-8"))
            if rec.get("stage") == "OS" and rec.get("status") == "ACTIVE":
                return {"admitted": True, "alpha_id": alpha_id, "metrics": m}
        except Exception:
            pass
    return {"admitted": False, "reason": "TIMEOUT_SELF_CORRELATION"}

CADENCE_CATALOG: List[Dict[str, Any]] = [
    {
        "name": "MARKUP_PRICING_POWER_TOP500_D5_252",
        "universe": "TOP500",
        "decay": 5,
        "expression": "0.60 * group_zscore(ts_rank(sales / (cogs + 0.001 * cap), 252), subindustry) + 0.40 * group_zscore(- (close / (ts_mean(close, 5) + 0.001) - 1.0), subindustry)"
    },
    {
        "name": "WORKING_CAP_TURNOVER_TOP200_D5_252",
        "universe": "TOP200",
        "decay": 5,
        "expression": "0.60 * group_zscore(ts_rank(sales / (assets - liabilities_curr + 0.001 * cap), 252), subindustry) + 0.40 * group_zscore(- (close / (ts_mean(close, 5) + 0.001) - 1.0), subindustry)"
    },
    {
        "name": "ASSET_TURNOVER_TOP500_D5_252",
        "universe": "TOP500",
        "decay": 5,
        "expression": "0.60 * group_zscore(ts_rank(sales / (assets + 0.001 * cap), 252), subindustry) + 0.40 * group_zscore(- (close / (ts_mean(close, 5) + 0.001) - 1.0), subindustry)"
    },
    {
        "name": "CAPEX_ASSETS_TOP500_D5_252",
        "universe": "TOP500",
        "decay": 5,
        "expression": "0.60 * group_zscore(- ts_rank(capex / (assets + 0.001 * cap), 252), subindustry) + 0.40 * group_zscore(- (close / (ts_mean(close, 5) + 0.001) - 1.0), subindustry)"
    },
    {
        "name": "FX_TRANS_ASSETS_TOP500_D5_252",
        "universe": "TOP500",
        "decay": 5,
        "expression": "0.60 * group_zscore(ts_rank(fn_oth_income_loss_fx_transaction_and_tax_translation_adj_a / (assets + 0.001 * cap), 252), subindustry) + 0.40 * group_zscore(- (close / (ts_mean(close, 5) + 0.001) - 1.0), subindustry)"
    }
]

def main() -> None:
    client = init_authenticated_client()
    assert client.is_authenticated, "Invariant failed: unauthenticated"
    assert len(CADENCE_CATALOG) > 0, "Cadence catalog must not be empty"

    print("Checking daily submission status...", flush=True)
    if has_submitted_today(client):
        print("Daily submission target already satisfied for today (UTC).", flush=True)
        return

    print("Executing daily cadence submission...", flush=True)
    for candidate in CADENCE_CATALOG:
        name = candidate["name"]
        print(f"Testing candidate: {name}...", flush=True)
        sim_id = dispatch_candidate_simulation(client, candidate)
        if not sim_id:
            continue

        alpha_id = poll_simulation_result(client, sim_id)
        if not alpha_id:
            continue

        result = verify_and_submit_alpha(client, alpha_id)
        if result.get("admitted"):
            print(f"Successfully admitted daily alpha {alpha_id} ({name})!", flush=True)
            return
        time.sleep(2)

if __name__ == "__main__":
    main()
