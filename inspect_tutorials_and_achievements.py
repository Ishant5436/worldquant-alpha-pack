#!/usr/bin/env python3
"""
Inspect WorldQuant BRAIN Tutorials, Achievements, and Progress.
Deterministic Safety Standards: Functions <= 60 lines, assertion density >= 2.
"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brain_client import BrainAPIClient

def fetch_achievements(client: BrainAPIClient):
    """Fetches global achievements and self achievements."""
    assert client.is_authenticated, "Client must be authenticated"

    r_all = client.session.get("https://api.worldquantbrain.com/achievements")
    all_ach = json.loads(r_all.read().decode())

    r_self = client.session.get("https://api.worldquantbrain.com/users/self/achievements")
    self_ach = json.loads(r_self.read().decode())

    assert isinstance(all_ach, list), "all_ach must be list"
    assert isinstance(self_ach, list), "self_ach must be list"
    return all_ach, self_ach

def fetch_tutorials(client: BrainAPIClient):
    """Fetches available tutorial tracks and pages."""
    assert client.is_authenticated, "Client must be authenticated"

    r_tut = client.session.get("https://api.worldquantbrain.com/tutorials")
    tut_data = json.loads(r_tut.read().decode())
    assert "results" in tut_data, "Malformed tutorial data"
    return tut_data["results"]

def main():
    client = BrainAPIClient("panchaleshant@gmail.com", "punpe7-bemfiw-gyjwyW")
    assert client.authenticate(), "Authentication failed"

    all_ach, self_ach = fetch_achievements(client)
    self_map = {a.get("id"): a for a in self_ach}

    print("=== GLOBAL ACHIEVEMENTS & USER STATUS ===")
    for a in all_ach:
        aid = a.get("id")
        user_rec = self_map.get(aid)
        achieved_at = user_rec.get("achieved") if user_rec else None
        status_str = f"COMPLETED ({achieved_at})" if achieved_at else "INCOMPLETE"
        val = user_rec.get("value") if user_rec else 0
        tot = a.get("total")
        print(f"[{status_str}] {aid}: {a.get('name')} | {a.get('description')} (val={val}/{tot})")

    tuts = fetch_tutorials(client)
    print("\n=== TUTORIALS CATALOG ===")
    for t in tuts:
        tid = t.get("id")
        cat = t.get("category")
        pages = t.get("pages", [])
        print(f"\nTutorial Track: {tid} ({cat}) - {len(pages)} pages")
        for p in pages:
            pid = p.get("id")
            title = p.get("title")
            dur = p.get("duration")
            print(f"  - Page: {pid} | {title} ({dur})")

if __name__ == "__main__":
    main()
