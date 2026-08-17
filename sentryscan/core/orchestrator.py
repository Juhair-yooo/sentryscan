"""
Runs the selected modules against an authorized target and collects results.
"""
from modules import recon, web_enum, web_vuln, sqli, ssl_tls, cve_lookup

MODULE_REGISTRY = {
    "recon": recon.run,
    "web_enum": web_enum.run,
    "web_vuln": web_vuln.run,
    "sqli": sqli.run,
    "ssl_tls": ssl_tls.run,
    "cve_lookup": cve_lookup.run,
}

DEFAULT_ORDER = ["recon", "web_enum", "web_vuln", "sqli", "ssl_tls", "cve_lookup"]


def run(target: str, modules=None) -> dict:
    modules = modules or DEFAULT_ORDER
    results = {}
    context = {}  # lets later modules reuse earlier findings (e.g. cve_lookup needs recon's service list)

    for name in modules:
        name = name.strip()
        if name not in MODULE_REGISTRY:
            print(f"[!] Unknown module '{name}', skipping")
            continue
        print(f"\n[*] Running {name}...")
        try:
            findings = MODULE_REGISTRY[name](target, context)
            results[name] = findings
            context[name] = findings
            print(f"[+] {name}: {len(findings)} finding(s)")
        except Exception as e:
            print(f"[!] {name} failed: {e}")
            results[name] = []

    return results
