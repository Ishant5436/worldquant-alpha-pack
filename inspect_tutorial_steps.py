#!/usr/bin/env python3
"""
Inspect all 27 Tutorial steps and requirements.
Deterministic Safety Standards: Functions <= 60 lines, assertion density >= 2.
"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brain_client import BrainAPIClient

def fetch_tutorial_details(client: BrainAPIClient):
    """Fetches full tutorial hierarchy and steps."""
    assert client.is_authenticated, "Client must be authenticated"
    
    r_sum = client.session.get("https://api.worldquantbrain.com/users/self/tutorial/summary")
    sum_data = json.loads(r_sum.read().decode())
    
    r_all = client.session.get("https://api.worldquantbrain.com/tutorials")
    all_data = json.loads(r_all.read().decode())
    
    assert isinstance(sum_data, dict), "sum_data must be dict"
    assert "results" in all_data, "all_data must contain results"
    return sum_data, all_data["results"]

def inspect_individual_steps(client: BrainAPIClient, pages):
    """Fetches individual step specifications for tutorial pages."""
    assert client.is_authenticated, "Client must be authenticated"
    assert isinstance(pages, list), "pages must be list"
    
    steps_info = []
    for p in pages:
        pid = p.get("id")
        try:
            r = client.session.get(f"https://api.worldquantbrain.com/tutorials/{pid}")
            p_data = json.loads(r.read().decode())
            steps_info.append(p_data)
        except Exception as e:
            print(f"Error fetching page {pid}: {e}")
    return steps_info

def main():
    email = os.environ.get("BRAIN_EMAIL", "panchaleshant@gmail.com")
    password = os.environ.get("BRAIN_PASSWORD", "punpe7-bemfiw-gyjwyW")
    client = BrainAPIClient(email=email, password=password)
    assert client.authenticate(), "Authentication failed"

    sum_data, tuts = fetch_tutorial_details(client)
    print("=== TUTORIAL SUMMARY ===")
    print(json.dumps(sum_data, indent=2))

    for t in tuts:
        tid = t.get("id")
        pages = t.get("pages", [])
        print(f"\n================ TRACK: {tid} ({t.get('name')}) ================")
        print(f"Description: {t.get('description')}")
        for idx, p in enumerate(pages):
            pid = p.get("id")
            title = p.get("title")
            print(f"\n--- Step {idx} (ID: {pid}): {title} ---")
            try:
                r = client.session.get(f"https://api.worldquantbrain.com/tutorials/{pid}")
                p_content = json.loads(r.read().decode())
                # print relevant task or question
                task = p_content.get("task", {})
                content = p_content.get("content", "")
                checks = p_content.get("checks", [])
                print(f"Task: {json.dumps(task)}")
                if checks:
                    print(f"Checks: {json.dumps(checks)}")
                if content:
                    # print first 300 chars of content
                    clean_content = content.replace("\n", " ")[:200]
                    print(f"Snippet: {clean_content}...")
            except Exception as e:
                print(f"Could not load details for {pid}: {e}")

if __name__ == "__main__":
    main()
