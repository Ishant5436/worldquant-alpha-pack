#!/usr/bin/env python3
"""
WorldQuant BRAIN - Grandmaster Fleet Monitor Daemon.
Queries live API endpoints to track Out-of-Sample (OS) health and competition scoring.

Deterministic Safety Invariants:
- Gerard Holzmann Power of 10 rules.
- Functions <= 60 lines.
- Assertion density >= 2 per function.
"""
import json
import os
import sys
from typing import Dict, Any, List

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brain_client import BrainAPIClient

def fetch_live_fleet(client: BrainAPIClient) -> List[Dict[str, Any]]:
    """Fetches all active out-of-sample alphas from the BRAIN platform."""
    assert client.is_authenticated, "Authentication invariant failed"
    assert client.session is not None, "Session invariant failed"

    alphas: List[Dict[str, Any]] = []
    offset = 0
    limit = 100
    for _ in range(10):
        url = f"https://api.worldquantbrain.com/users/self/alphas?stage=OS&limit={limit}&offset={offset}"
        resp = client.session.get(url, timeout=20)
        assert resp.status == 200, f"HTTP Error {resp.status}"
        data = json.loads(resp.read().decode("utf-8"))
        results = data.get("results", [])
        alphas.extend(results)
        if len(results) < limit or len(alphas) >= data.get("count", 0):
            break
        offset += limit
    return alphas

def fetch_competition_progress(client: BrainAPIClient) -> Dict[str, Any]:
    """Fetches user competition progress and leaderboard standing."""
    assert client.is_authenticated, "Authentication invariant failed"
    assert client.session is not None, "Session invariant failed"

    url = "https://api.worldquantbrain.com/users/self/competitions"
    resp = client.session.get(url, timeout=15)
    assert resp.status == 200, f"HTTP Error {resp.status}"

    data = json.loads(resp.read().decode("utf-8"))
    results = data.get("results", [])
    assert len(results) > 0, "No enrolled competitions found"
    return results[0]

def display_dashboard(fleet: List[Dict[str, Any]], comp: Dict[str, Any]) -> None:
    """Formats and prints the executive quantitative monitoring dashboard."""
    assert isinstance(fleet, list), "Fleet must be a list"
    assert isinstance(comp, dict), "Competition metadata must be a dict"

    lb = comp.get("leaderboard", {})
    comp_name = comp.get("name", "Challenge - India")
    help_text = comp.get("helpText", "")

    print("\n" + "=" * 78)
    print("      WORLDQUANT BRAIN — GRANDMASTER FLEET MONITOR & OS AUDITOR")
    print("=" * 78)
    print(f"User: {lb.get('user', 'UNKNOWN')} | Tier: GOLD | Competition: {comp_name}")
    print(f"Country Rank: #{lb.get('rank', 'N/A')} | Total Score: {lb.get('score', 0):.2f}")
    if "isScore" in lb:
        print(f"IS Score: {lb.get('isScore', 0):,.1f} | Uniqueness: {lb.get('uniquenessScore', 0):.2f} | Days of Submission: {lb.get('daysOfSubmission', 0)}")
    print("-" * 78)
    pct = (len(fleet) / 50.0) * 100.0
    print(f"Total Out-of-Sample (OS) Alphas: {len(fleet)} / 50 ({pct:.1f}% Grandmaster Milestone)")

    active_count = sum(1 for a in fleet if a.get("status") == "ACTIVE")
    print(f"Active Status Rate: {active_count}/{len(fleet)} ({(active_count/max(len(fleet),1))*100:.1f}%) | Buffer: +{len(fleet)-50} Alphas")
    if help_text:
        print(f"Status Note: {help_text}")
    print("-" * 78)
    print(f"{'#':<3} | {'Alpha ID':<9} | {'Univ':<7} | {'Decay':<5} | {'IS Sharpe':<9} | {'IS Fit':<6} | {'Turnover':<8} | {'Status'}")
    print("-" * 78)

    for i, a in enumerate(fleet[:15], 1):
        aid = a.get("id", "")
        sett = a.get("settings", {})
        u = sett.get("universe", "")
        d = sett.get("decay", 0)
        m = a.get("is", {})
        s = m.get("sharpe", 0.0)
        f = m.get("fitness", 0.0)
        to = m.get("turnover", 0.0)
        stat = a.get("status", "")
        print(f"{i:<3} | {aid:<9} | {u:<7} | {d:<5} | {s:<9.2f} | {f:<6.2f} | {to*100:<7.1f}% | {stat}")

    if len(fleet) > 15:
        print(f"... and {len(fleet) - 15} additional active Out-of-Sample alphas.")
    print("=" * 78 + "\n")

def main() -> None:
    """Execution entry point."""
    email = os.environ.get("BRAIN_EMAIL", "panchaleshant@gmail.com")
    password = os.environ.get("BRAIN_PASSWORD", "punpe7-bemfiw-gyjwyW")
    client = BrainAPIClient(email=email, password=password)
    assert client.authenticate(), "Authentication failed. Check credentials."

    fleet = fetch_live_fleet(client)
    comp = fetch_competition_progress(client)
    display_dashboard(fleet, comp)

if __name__ == "__main__":
    main()
