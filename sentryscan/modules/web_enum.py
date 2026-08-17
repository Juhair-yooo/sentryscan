"""
gobuster wrapper: directory/file enumeration on web ports found by recon.
"""
import subprocess
import shutil

DEFAULT_WORDLIST = "/usr/share/wordlists/dirb/common.txt"


def run(target: str, context: dict) -> list:
    if not shutil.which("gobuster"):
        return [{"error": "gobuster not found on PATH"}]

    web_ports = _web_ports_from_recon(context.get("recon", []))
    if not web_ports:
        web_ports = [(80, "http"), (443, "https")]  # fallback guess if recon wasn't run first

    findings = []
    for port, scheme in web_ports:
        url = f"{scheme}://{target}:{port}"
        cmd = ["gobuster", "dir", "-u", url, "-w", DEFAULT_WORDLIST, "-q", "-t", "30"]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            for line in proc.stdout.splitlines():
                if line.strip():
                    findings.append({"url": url, "path": line.strip()})
        except subprocess.TimeoutExpired:
            findings.append({"url": url, "error": "gobuster timed out"})
    return findings


def _web_ports_from_recon(recon_findings: list):
    ports = []
    for f in recon_findings:
        if f.get("service") in ("http", "https"):
            ports.append((int(f["port"]), f["service"]))
    return ports
