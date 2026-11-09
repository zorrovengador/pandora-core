"""Pure decision gate for independently observed Composio route status.

Inputs are operator observations from THIS runtime, not connection discovery or auth.
Never use this module's output as proof of a live connection.
"""

ALLOWED_FALLBACK = frozenset({
    "executable_absent", "authentication_unavailable", "connection_unavailable",
    "technical_failure",
})
BLOCKED = frozenset({
    "authorization_denied", "insufficient_permissions", "wrong_account",
    "policy_denied",
})


def choose_route(cli_status, expected_identity, mcp_status=None, mcp_identity=None):
    """Return (route, reason). None means STOP; never select an unknown tenant."""
    if (not isinstance(expected_identity, tuple) or len(expected_identity) != 2
            or not all(isinstance(v, str) and v.strip() for v in expected_identity)):
        return None, "identity_unverified"
    if cli_status == "usable":
        return "cli", "cli_priority"
    if cli_status in BLOCKED:
        return None, "cli_authorization_or_policy_block"
    if cli_status not in ALLOWED_FALLBACK:
        return None, "cli_cause_uncertain"
    if mcp_status != "usable":
        return None, "mcp_not_verified"
    if not mcp_identity or mcp_identity != expected_identity:
        return None, "mcp_identity_unverified_or_mismatched"
    return "mcp", "cli_unavailable_same_identity"
