"""
TLS/SSL config check via nmap's ssl-enum-ciphers script (avoids needing
testssl.sh as an extra dependency on top of the standard Kali toolset).
"""
import subprocess


def run(target: str, context: dict) -> list:
    https_ports = [f["port"] for f in context.get("recon", []) if f.get("service") == "https"] or ["443"]

    findings = []
    for port in https_ports:
        cmd = ["nmap", "-Pn", "-p", str(port), "--script", "ssl-enum-ciphers", target]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        for line in proc.stdout.splitlines():
            line = line.strip()
            if "least strength" in line.lower() or (line.startswith("|") and ("TLS" in line or "SSL" in line)):
                findings.append({"port": port, "finding": line})
    return findings
