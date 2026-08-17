"""
sqlmap wrapper - DETECTION ONLY. Confirms injectable parameters, does not
dump data, drop to a shell, or write files on the target. If a finding here
needs to go further, do that manually and deliberately as part of your
engagement - not via an unattended script.
"""
import subprocess
import shutil


def run(target: str, context: dict) -> list:
    if not shutil.which("sqlmap"):
        return [{"error": "sqlmap not found on PATH"}]

    url = f"http://{target}/"
    cmd = [
        "sqlmap", "-u", url,
        "--batch", "--crawl=1", "--forms",
        "--level=1", "--risk=1",
        "--disable-coloring",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=900)

    findings = []
    for line in proc.stdout.splitlines():
        lower = line.lower()
        if "is vulnerable" in lower or ("parameter" in lower and "injectable" in lower):
            findings.append({"finding": line.strip()})
    return findings
