#!/usr/bin/env python3
"""Portable Pandora budget monitor.

Reads only non-secret configuration and writes a current status JSON under the
active Hermes home. It prints a stable threshold key for cron monitor gating.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HOME = Path(os.environ.get("HERMES_HOME", str(Path.home() / ".hermes")))
CONFIG = HOME / "config" / "budget_alerts.json"
STATUS = HOME / "reports" / "budget" / "latest.json"
HERMES_CONFIG = HOME / "config.yaml"


def provider() -> str:
    inside_model = False
    for line in HERMES_CONFIG.read_text(encoding="utf-8").splitlines():
        if re.match(r"^model:\s*$", line):
            inside_model = True
            continue
        if inside_model and re.match(r"^[^\s#].*:\s*", line):
            break
        if inside_model:
            match = re.match(r"^\s+provider:\s*['\"]?(.+?)['\"]?\s*$", line)
            if match:
                return match.group(1).strip().lower()
    return "unknown"


def openrouter_usage() -> float:
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise RuntimeError("OPENROUTER_API_KEY unavailable")
    request = urllib.request.Request(
        "https://openrouter.ai/api/v1/key", headers={"Authorization": f"Bearer {key}"}
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        value = json.load(response).get("data", {}).get("usage_monthly")
    if not isinstance(value, (int, float)):
        raise RuntimeError("OpenRouter did not return usage_monthly")
    return float(value)


def local_nous_estimate() -> float:
    result = subprocess.run(["hermes", "insights", "--days", "30"], capture_output=True, text=True)
    match = re.search(r"Estimated:\s*~?\$([0-9]+(?:\.[0-9]+)?)", result.stdout)
    if result.returncode or not match:
        raise RuntimeError("Hermes local estimate unavailable")
    return float(match.group(1))


def main() -> int:
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    budget = float(cfg["monthly_budget_usd"])
    active = provider()
    now = datetime.now(timezone.utc)
    state = {"checked_at_utc": now.isoformat(), "billing_period_utc": now.strftime("%Y-%m"), "provider": active, "budget_usd": budget, "state": "inactive", "band": 0, "spend_usd": None, "percent": None, "source": None, "note": None}
    try:
        if active == "openrouter":
            spend, source = openrouter_usage(), "openrouter_usage_monthly_exact"
        elif active in {"nous", "nous portal", "nous-portal"}:
            spend, source = local_nous_estimate(), "hermes_local_estimate_rolling_30d"
            state["note"] = cfg["nous"]["warning"]
        else:
            spend, source = None, None
            state["note"] = "Provider is not monitored by this skill."
        if spend is not None:
            percent = spend / budget * 100 if budget else 0.0
            band = max((int(x) for x in cfg["thresholds_percent"] if percent >= float(x)), default=0)
            state.update({"state": "active", "spend_usd": round(spend, 6), "percent": round(percent, 2), "band": band, "source": source})
    except (RuntimeError, urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError) as exc:
        state.update({"state": "unavailable", "note": str(exc)})
    STATUS.parent.mkdir(parents=True, exist_ok=True)
    STATUS.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"period={state['billing_period_utc']} provider={active} state={state['state']} band={state['band']} source={state['source'] or 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
