#!/usr/bin/env python3
"""
Unit and Mock Tests for the WorldQuant BRAIN API Client.
Deterministic Safety Standards: Functions <= 60 lines, assertion density >= 2.
"""
import json
import os
import sys
import pytest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from brain_client import BrainAPIClient


def test_brain_client_unconfigured():
    """Verify client handles missing credentials gracefully."""
    with patch.dict(os.environ, {}, clear=True):
        client = BrainAPIClient(email="", password="")
        assert client.is_configured is False
        res = client.authenticate()
        assert res is False


def test_brain_client_authenticate_success():
    """Verify successful authentication handshake against WorldQuant BRAIN API."""
    client = BrainAPIClient(email="quant@example.com", password="secure_pass")
    mock_response = MagicMock()
    mock_response.status = 201

    with patch.object(client.session, "post", return_value=mock_response):
        success = client.authenticate()
        assert success is True, "Authentication must succeed with valid response"
        assert client.is_authenticated is True


def test_brain_client_simulate_dispatch():
    """Verify dispatching a simulation payload formats request correctly."""
    client = BrainAPIClient(email="quant@example.com", password="secure_pass")
    client.is_authenticated = True

    mock_resp = MagicMock()
    mock_resp.status = 201
    mock_resp.headers = {"Location": "https://api.worldquantbrain.com/simulations/sim_12345"}

    alpha_spec = {
        "expression": "rank(close - open)",
        "settings": {
            "Region": "USA",
            "Universe": "TOP3000",
            "Neutralization": "Subindustry",
            "Truncation": "0.08",
        },
    }

    with patch.object(client.session, "post", return_value=mock_resp):
        sim_id = client.dispatch_simulation(alpha_spec)
        assert sim_id == "sim_12345", f"Expected sim_12345, got {sim_id}"


def test_brain_client_poll_simulation():
    """Verify polling simulation results extracts performance metrics."""
    client = BrainAPIClient(email="quant@example.com", password="secure_pass")
    client.is_authenticated = True

    payload = {
        "status": "COMPLETED",
        "alpha": {
            "is": {
                "sharpe": 1.45,
                "fitness": 1.20,
                "turnover": 0.35,
                "margin": 0.0015,
            }
        },
    }
    mock_resp = MagicMock()
    mock_resp.status = 200
    mock_resp.read.return_value = json.dumps(payload).encode("utf-8")

    with patch.object(client.session, "get", return_value=mock_resp):
        res = client.poll_simulation("sim_12345", timeout=5)
        assert res["status"] == "COMPLETED"
        assert res["sharpe"] == 1.45
        assert res["turnover"] == 0.35


def test_submitted_alphas_portfolio_structure():
    """Verify submitted_alphas.json holds valid active OS alphas."""
    sub_path = os.path.join(os.path.dirname(__file__), "..", "submitted_alphas.json")
    assert os.path.exists(sub_path), "submitted_alphas.json must exist"
    with open(sub_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["submitted_count"] == 13, f"Expected 13 alphas, got {data['submitted_count']}"
    assert len(data["alphas"]) == 13, f"Expected 13 alpha records, got {len(data['alphas'])}"
    for a in data["alphas"]:
        assert a["stage"] == "OS"
        assert a["status"] == "ACTIVE"
        assert a["metrics"]["sharpe"] >= 1.25
        assert a["metrics"]["fitness"] >= 1.00

