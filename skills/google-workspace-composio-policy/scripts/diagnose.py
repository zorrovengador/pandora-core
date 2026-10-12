"""Read-only, non-network evidence diagnostic. Never probes or reads credentials."""
import argparse
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import shutil

SERVICES = {"gmail", "calendar", "drive", "docs", "sheets", "slides"}
ROUTES = {"connector", "cli", "mcp"}


def diagnose(record, instance, service, now=None, cli_present=False):
    """Evidence is an operator attestation, never live authorization/health."""
    result = {"status": "pending", "live_verified": False,
              "cli_present": cli_present, "connector_discovery": "conversation_required",
              "mcp_discovery": "conversation_required"}
    def fail(reason):
        return {**result, "reason": reason}
    if not isinstance(record, dict):
        return fail("record_missing_or_invalid")
    if set(record) != {"schema_version", "instance_id", "composio_account_id",
                       "composio_project_id", "google_account", "route", "services"}:
        return fail("record_schema_invalid")
    if record["schema_version"] != 1:
        return fail("record_schema_invalid")
    if record["instance_id"] != instance:
        return fail("instance_mismatch")
    for field in ("instance_id", "composio_account_id", "composio_project_id", "google_account"):
        if not isinstance(record[field], str) or not record[field].strip():
            return fail("identity_missing")
    route = record["route"]
    if not isinstance(route, str) or route not in ROUTES:
        return fail("route_invalid")
    services = record["services"]
    if not isinstance(services, dict) or not set(services) <= SERVICES:
        return fail("services_invalid")
    item = services.get(service)
    if not isinstance(item, dict) or set(item) != {"connection_id", "google_account", "status", "verified_at", "evidence_ref"}:
        return fail("service_pending_or_invalid")
    if item["status"] != "verified_read":
        return fail("service_not_verified")
    if item["google_account"] != record["google_account"]:
        return fail("google_account_mismatch")
    for field in ("connection_id", "evidence_ref"):
        if not isinstance(item[field], str) or not item[field].strip():
            return fail("connection_or_evidence_missing")
    try:
        at = datetime.fromisoformat(item["verified_at"].replace("Z", "+00:00"))
        if at.tzinfo is None:
            return fail("timestamp_invalid")
    except (ValueError, TypeError, AttributeError):
        return fail("timestamp_invalid")
    now = now or datetime.now(timezone.utc)
    if at > now or now - at > timedelta(hours=24):
        return fail("evidence_stale_or_future")
    if route == "cli" and not cli_present:
        return fail("selected_cli_missing")
    return {**result, "status": "recent_recorded_evidence", "route": route,
            "reason": "live_read_required_before_operation"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--instance", required=True, help="Expected non-secret runtime identity")
    parser.add_argument("--service", required=True, choices=sorted(SERVICES))
    args = parser.parse_args()
    home = os.environ.get("HERMES_HOME")
    record = None
    if home:
        try:
            path = Path(home) / "integrations" / "composio-google.json"
            # Bound input; malformed records never echo supplied values or exceptions.
            if path.stat().st_size <= 65536:
                record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError, UnicodeError):
            pass
    result = diagnose(record, args.instance, args.service,
                      cli_present=shutil.which("composio") is not None)
    if not home:
        result["reason"] = "hermes_home_required"
    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"] == "recent_recorded_evidence" else 2


if __name__ == "__main__":
    raise SystemExit(main())
