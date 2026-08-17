"""
nikto wrapper: web server misconfiguration / known vuln scan.
"""
import subprocess
import shutil


def run(target: str, context: dict) -> list:
    if not shutil.which("nikto"):
        return [{"error": "nikto not found on PATH"}]

    cmd = ["nikto", "-h", target, "-Format", "txt", "-ask", "no"]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=900)

    findings = []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if line.startswith("+") and "Target" not in line and "Start Time" not in line:
            findings.append({"finding": line.lstrip("+ ").strip()})
    return findings
