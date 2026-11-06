#!/usr/bin/env python3
"""
WorldQuant BRAIN - Interactive Tutorial Pipeline Automator.
Automates tutorial step progression from Step 8 onwards towards clearing all 27 steps.

Deterministic Safety Standards:
- Gerard Holzmann Power of 10 Safety Invariants.
- Functions <= 60 lines.
- Assertion density >= 2 per function.
- Bounded loops.
"""
import json
import os
import sys
import time
import urllib.request
from typing import Dict, Any, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brain_client import BrainAPIClient

def init_authenticated_client() -> BrainAPIClient:
    """Initializes and authenticates BRAIN API client."""
    email = os.environ.get("BRAIN_EMAIL", "panchaleshant@gmail.com")
    password = os.environ.get("BRAIN_PASSWORD", "punpe7-bemfiw-gyjwyW")
    assert len(email) > 0, "Email parameter must not be empty"
    assert len(password) > 0, "Password parameter must not be empty"

    client = BrainAPIClient(email=email, password=password)
    assert client.authenticate(), "Authentication failed"
    return client

def patch_current_step(client: BrainAPIClient, step_index: int) -> Dict[str, Any]:
    """Patches active currentStep in tutorial summary."""
    assert client.is_authenticated, "Client unauthenticated"
    assert 0 <= step_index <= 27, "Invalid step index"

    req = urllib.request.Request(
        "https://api.worldquantbrain.com/users/self/tutorial/summary",
        data=json.dumps({"currentStep": step_index}).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="PATCH"
    )
    client.session.opener.open(req)
    r = client.session.get("https://api.worldquantbrain.com/users/self/tutorial/summary")
    return json.loads(r.read().decode())

def simulate_tutorial_alpha(client: BrainAPIClient, expr: str, decay: int = 10, neut: str = "MARKET") -> Optional[str]:
    """Simulates a lightweight tutorial alpha and returns alpha ID."""
    assert client.is_authenticated, "Client unauthenticated"
    assert len(expr) > 0, "Expression must not be empty"

    payload = {
        "type": "REGULAR",
        "settings": {
            "instrumentType": "EQUITY",
            "region": "USA",
            "universe": "TOP3000",
            "delay": 1,
            "decay": decay,
            "neutralization": neut,
            "truncation": 0.08,
            "pasteurization": "ON",
            "unitHandling": "VERIFY",
            "nanHandling": "OFF",
            "language": "FASTEXPR",
            "visualization": False
        },
        "regular": expr
    }

    resp = client.session.post("https://api.worldquantbrain.com/simulations", json_data=payload)
    loc = resp.headers.get("Location")
    assert loc is not None, "Missing Location header"

    for _ in range(30):
        time.sleep(4)
        r = client.session.get(loc)
        data = json.loads(r.read().decode())
        if "alpha" in data:
            return data["alpha"]
    return None

def verify_step(client: BrainAPIClient, alpha_id: str) -> Dict[str, Any]:
    """Verifies tutorial criteria against simulated alpha."""
    assert client.is_authenticated, "Client unauthenticated"
    assert len(alpha_id) > 0, "alpha_id must not be empty"

    r = client.session.get(f"https://api.worldquantbrain.com/alphas/{alpha_id}/tutorial")
    checks = json.loads(r.read().decode())
    r_sum = client.session.get("https://api.worldquantbrain.com/users/self/tutorial/summary")
    summary = json.loads(r_sum.read().decode())
    return {"checks": checks, "summary": summary}

def main():
    print("=== WorldQuant BRAIN: Tutorial Step 8 Solver ===", flush=True)
    client = init_authenticated_client()

    # Step 8 requires vwap/close with turnover < 70% (Decay 10)
    print("[*] Patching currentStep to 8...", flush=True)
    sum_data = patch_current_step(client, 8)
    print(f"    Current summary: currentStep={sum_data.get('currentStep')}, maxUnlocked={sum_data.get('maxUnlockedStep')}")

    print("[*] Simulating tutorial alpha: vwap/close (decay 10)...", flush=True)
    alpha_id = simulate_tutorial_alpha(client, "vwap/close", decay=10, neut="MARKET")
    print(f"    Simulated Alpha ID: {alpha_id}")

    if alpha_id:
        v_res = verify_step(client, alpha_id)
        print("    Verification Checks:", json.dumps(v_res["checks"], indent=2))
        print("    New Tutorial Summary:", json.dumps(v_res["summary"], indent=2))

if __name__ == "__main__":
    main()
