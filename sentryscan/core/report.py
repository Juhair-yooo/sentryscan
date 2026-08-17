"""
Turns the orchestrator's results dict into a single Markdown report.
"""
import os
from datetime import datetime


def generate(target: str, results: dict, output_dir: str = "reports") -> str:
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_target = target.replace("/", "_").replace(":", "_")
    path = os.path.join(output_dir, f"{safe_target}_{timestamp}.md")

    lines = [f"# SentryScan Report - {target}", f"Generated: {datetime.now().isoformat()}", ""]

    total_findings = sum(len(v) for v in results.values())
    lines.append(f"**Total findings: {total_findings}**\n")

    for module, findings in results.items():
        lines.append(f"## {module} ({len(findings)})")
        if not findings:
            lines.append("_No findings._\n")
            continue
        for f in findings:
            lines.append(f"- {_format_finding(f)}")
        lines.append("")

    with open(path, "w") as f:
        f.write("\n".join(lines))

    return path


def _format_finding(f: dict) -> str:
    if isinstance(f, dict):
        return " | ".join(f"{k}: {v}" for k, v in f.items())
    return str(f)
