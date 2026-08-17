"""
nmap wrapper: service/version scan. This is the foundation module - other
modules read its output via the shared context dict.
"""
import subprocess
import xml.etree.ElementTree as ET


def run(target: str, context: dict) -> list:
    cmd = ["nmap", "-sV", "-Pn", "-oX", "-", target]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    return _parse(proc.stdout)


def _parse(xml_output: str) -> list:
    findings = []
    if not xml_output.strip():
        return findings
    root = ET.fromstring(xml_output)
    for host in root.findall("host"):
        for port in host.findall(".//port"):
            state = port.find("state")
            if state is None or state.get("state") != "open":
                continue
            service = port.find("service")
            findings.append({
                "port": port.get("portid"),
                "protocol": port.get("protocol"),
                "service": service.get("name") if service is not None else "unknown",
                "product": service.get("product", "") if service is not None else "",
                "version": service.get("version", "") if service is not None else "",
            })
    return findings
