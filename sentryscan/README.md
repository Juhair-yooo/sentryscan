# SentryScan

Automated vulnerability discovery pipeline for Kali Linux. Wraps `nmap`, `gobuster`,
`nikto`, `sqlmap`, and `searchsploit` into one pipeline, with a built-in authorization
check so it only ever runs against targets you've explicitly whitelisted.

## ⚠️ Authorized use only

This tool actively probes live systems. Only point it at:
- Systems you own (personal lab VMs)
- Infrastructure you have explicit written authorization to test
- Public practice targets built for this (scanme.nmap.org, an active HTB/THM box)

Scanning or testing anything else without permission is illegal in most jurisdictions.
`core/target_guard.py` refuses to run against anything not listed in
`config/targets.yaml` — that's a safety net against fat-fingering a target, not a
substitute for having real authorization.

## What it does

| Module | Tool | Finds |
|---|---|---|
| `recon` | nmap | Open ports, services, versions |
| `web_enum` | gobuster | Hidden directories/files on web servers |
| `web_vuln` | nikto | Known web server misconfigs/vulns |
| `sqli` | sqlmap | SQL injection points (**detection only** — no dump, no shell) |
| `ssl_tls` | nmap `ssl-enum-ciphers` | Weak TLS/SSL config |
| `cve_lookup` | searchsploit | Known CVEs matching detected service versions |

Later modules can read earlier modules' output (e.g. `cve_lookup` uses `recon`'s
service list) via a shared `context` dict. Everything gets written to one Markdown
report per run.

## Requirements

- Kali Linux (or any distro with `nmap`, `gobuster`, `nikto`, `sqlmap`, `searchsploit` on PATH)
- Python 3.9+

## Setup

```bash
git clone <your-repo-url>
cd sentryscan
pip install -r requirements.txt
cp config/targets.yaml.example config/targets.yaml
# edit config/targets.yaml — add each target + why you're authorized to test it
```

## Usage

```bash
python3 main.py --target 192.168.56.101
python3 main.py --target 192.168.56.101 --modules recon,web_vuln,sqli
python3 main.py --target 192.168.56.101 --output reports/
```

## Adding a target

Edit `config/targets.yaml`:

```yaml
targets:
  - host: 192.168.56.101
    type: lab
    authorized: true
    note: "Metasploitable2 VM, local lab"
```

Nothing runs unless `authorized: true` is set for that exact host.

## Adding a module

Each file in `modules/` is a plain function `run(target, context) -> list[dict]`.
Drop a new file in, register it in `core/orchestrator.py`'s `MODULE_REGISTRY`, done.

## Roadmap — not included yet, on purpose

- **Active exploitation.** This build is detection-and-report only. Confirmed findings
  (e.g. a sqlmap-flagged injectable parameter) are for you to act on manually, not for
  the pipeline to auto-exploit unattended.
- **XSS / CSRF / IDOR / auth-bypass modules.** These need app-specific logic rather
  than an off-the-shelf tool — tell me the specifics of what you want checked and I'll
  build the module.

## Making the repo private

```bash
git init && git add -A && git commit -m "Initial scaffold"
# with GitHub CLI:
gh repo create sentryscan --private --source=. --push
# or manually: create a private repo on github.com, then
git remote add origin git@github.com:<you>/sentryscan.git
git branch -M main && git push -u origin main
```
