"""
Gatekeeper: nothing in this toolkit runs against a host unless it's
explicitly whitelisted in config/targets.yaml with authorized: true.
"""
import sys
import os
import yaml

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "targets.yaml")


def _load_targets():
    if not os.path.exists(CONFIG_PATH):
        sys.exit(
            f"[!] No targets.yaml found at {CONFIG_PATH}\n"
            f"    Run: cp config/targets.yaml.example config/targets.yaml"
        )
    with open(CONFIG_PATH, "r") as f:
        data = yaml.safe_load(f) or {}
    return data.get("targets", [])


def require_authorized(host: str) -> dict:
    """Returns the target entry if authorized, otherwise exits the program."""
    targets = _load_targets()
    for entry in targets:
        if entry.get("host") == host:
            if entry.get("authorized") is True:
                print(f"[+] Target authorized: {host} - {entry.get('note', 'no note')}")
                return entry
            sys.exit(
                f"[!] '{host}' is listed but authorized: false - "
                f"flip it to true in config/targets.yaml only once you actually have permission."
            )
    sys.exit(
        f"[!] '{host}' is not in config/targets.yaml - refusing to scan.\n"
        f"    Add it there first, with a note on why you're authorized to test it."
    )
