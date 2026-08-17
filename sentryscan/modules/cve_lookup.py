"""
searchsploit wrapper - matches services/versions found by recon against the
local exploit-db mirror. This is purely a lookup against existing, already
public exploit-db entries; it doesn't generate or run anything itself.
"""
import subprocess
import shutil
import json


def run(target: str, context: dict) -> list:
    if not shutil.which("searchsploit"):
        return [{"error": "searchsploit not found on PATH"}]

    findings = []
    for f in context.get("recon", []):
        product, version = f.get("product", ""), f.get("version", "")
        if not product:
            continue
        query = f"{product} {version}".strip()
        cmd = ["searchsploit", "-j", query]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            data = json.loads(proc.stdout or "{}")
            for match in data.get("RESULTS_EXPLOIT", []):
                findings.append({
                    "service": query,
                    "exploit_title": match.get("Title"),
                    "edb_id": match.get("EDB-ID"),
                })
        except (subprocess.TimeoutExpired, json.JSONDecodeError):
            continue
    return findings
