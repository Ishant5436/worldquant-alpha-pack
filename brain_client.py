#!/usr/bin/env python3
"""
WorldQuant BRAIN Automated REST API Simulation Client.
Standard-library HTTP implementation with zero external dependencies.
Enforces Deterministic Safety Standards: Functions <= 60 lines, assertion density >= 2.
"""
import base64
import http.cookiejar
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Dict, Any, Optional

BASE_URL = "https://api.worldquantbrain.com"


class _BrainSession:
    """Lightweight session manager wrapping standard library urllib."""

    def __init__(self):
        self.cookie_jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie_jar))
        assert self.cookie_jar is not None, "Cookie jar initialization invariant failed"
        assert self.opener is not None, "Opener initialization invariant failed"

    def post(self, url: str, json_data: Optional[Dict[str, Any]] = None, auth: Optional[tuple] = None, timeout: int = 15):
        """Sends HTTP POST request with JSON payload and optional basic auth."""
        assert isinstance(url, str) and url.startswith("http"), "Invalid URL"
        assert timeout > 0, "Timeout must be positive"

        body = json.dumps(json_data).encode("utf-8") if json_data is not None else b""
        req = urllib.request.Request(url, data=body, method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("Accept", "application/json")

        if auth and len(auth) == 2:
            creds = f"{auth[0]}:{auth[1]}".encode("utf-8")
            b64_auth = base64.b64encode(creds).decode("ascii")
            req.add_header("Authorization", f"Basic {b64_auth}")

        return self.opener.open(req, timeout=timeout)

    def get(self, url: str, timeout: int = 10):
        """Sends HTTP GET request."""
        assert isinstance(url, str) and url.startswith("http"), "Invalid URL"
        assert timeout > 0, "Timeout must be positive"
        req = urllib.request.Request(url, method="GET")
        req.add_header("Accept", "application/json")
        return self.opener.open(req, timeout=timeout)


class BrainAPIClient:
    """Manages authenticated session and simulation lifecycle on WorldQuant BRAIN."""

    def __init__(self, email: Optional[str] = None, password: Optional[str] = None):
        user_email = email if email is not None else os.environ.get("BRAIN_EMAIL", "")
        user_pwd = password if password is not None else os.environ.get("BRAIN_PASSWORD", "")
        assert isinstance(user_email, str), "Email must be string"
        assert isinstance(user_pwd, str), "Password must be string"

        self.email = user_email.strip()
        self.password = user_pwd.strip()
        self.is_configured = bool(self.email and self.password)
        self.is_authenticated = False
        self.session = _BrainSession()

    def authenticate(self) -> bool:
        """Authenticates with BRAIN API endpoint via HTTP Basic Auth."""
        assert isinstance(self.is_configured, bool), "Configuration state invariant violated"
        if not self.is_configured:
            return False

        url = f"{BASE_URL}/authentication"
        try:
            resp = self.session.post(url, auth=(self.email, self.password), timeout=10)
            status_code = getattr(resp, "status", getattr(resp, "status_code", 200))
            if status_code in [200, 201]:
                self.is_authenticated = True
                return True
            return False
        except Exception:
            return False

    def dispatch_simulation(self, alpha_spec: Dict[str, Any]) -> Optional[str]:
        """Dispatches an alpha expression to WorldQuant BRAIN simulation cluster."""
        assert isinstance(alpha_spec, dict), "Alpha spec must be a dictionary"
        assert "expression" in alpha_spec, "Alpha spec missing expression"

        if not self.is_authenticated:
            return None

        url = f"{BASE_URL}/simulations"
        settings = alpha_spec.get("settings", {})
        payload = {
            "type": "REGULAR",
            "settings": {
                "instrumentType": "EQUITY",
                "region": settings.get("Region", "USA"),
                "universe": settings.get("Universe", "TOP3000"),
                "delay": 1,
                "decay": 0,
                "neutralization": settings.get("Neutralization", "Subindustry").upper(),
                "truncation": float(settings.get("Truncation", 0.08)),
                "pasteurization": "ON",
                "unitHandling": "VERIFY",
                "nanHandling": "OFF",
                "language": "FASTEXPR",
                "visualization": False,
            },
            "regular": alpha_spec["expression"],
        }
        try:
            resp = self.session.post(url, json_data=payload, timeout=15)
            status_code = getattr(resp, "status", getattr(resp, "status_code", 200))
            if status_code in [200, 201]:
                headers = getattr(resp, "headers", {})
                loc = headers.get("Location", "") if hasattr(headers, "get") else ""
                if loc:
                    return loc.rstrip("/").split("/")[-1]
                data = json.loads(resp.read().decode("utf-8")) if hasattr(resp, "read") else resp.json()
                return data.get("id") or data.get("simulation_id")
            return None
        except Exception:
            return None

    def poll_simulation(self, sim_id: str, timeout: int = 120) -> Dict[str, Any]:
        """Polls simulation status and returns completed alpha metrics."""
        assert isinstance(sim_id, str) and len(sim_id) > 0, "Invalid sim_id"
        assert timeout > 0, "Timeout must be positive"

        url = f"{BASE_URL}/simulations/{sim_id}"
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                resp = self.session.get(url, timeout=10)
                status_code = getattr(resp, "status", getattr(resp, "status_code", 200))
                if status_code == 200:
                    data = json.loads(resp.read().decode("utf-8")) if hasattr(resp, "read") else resp.json()
                    status = data.get("status", "UNKNOWN")
                    if status == "COMPLETED":
                        alpha_is = data.get("alpha", {}).get("is", {})
                        return {
                            "status": "COMPLETED",
                            "sharpe": float(alpha_is.get("sharpe", 0.0)),
                            "fitness": float(alpha_is.get("fitness", 0.0)),
                            "turnover": float(alpha_is.get("turnover", 0.0)),
                            "margin": float(alpha_is.get("margin", 0.0)),
                        }
                    elif status in ["ERROR", "FAILED"]:
                        return {"status": "FAILED", "error": data.get("message", "Simulation failed")}
            except Exception as err:
                return {"status": "ERROR", "error": str(err)}
            time.sleep(2)
        return {"status": "TIMEOUT", "error": "Polling timed out"}
