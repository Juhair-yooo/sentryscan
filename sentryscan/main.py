#!/usr/bin/env python3
"""
SentryScan - authorized-target vulnerability discovery pipeline.

Usage:
    python3 main.py --target 192.168.56.101
    python3 main.py --target 192.168.56.101 --modules recon,sqli
"""
import argparse
from core import target_guard, orchestrator, report


def main():
    parser = argparse.ArgumentParser(description="SentryScan vulnerability discovery pipeline")
    parser.add_argument("--target", required=True, help="Host/IP to scan (must be listed in config/targets.yaml)")
    parser.add_argument("--modules", help="Comma-separated module list (default: all)")
    parser.add_argument("--output", default="reports", help="Report output directory")
    args = parser.parse_args()

    target_guard.require_authorized(args.target)

    modules = args.modules.split(",") if args.modules else None
    results = orchestrator.run(args.target, modules)

    path = report.generate(args.target, results, args.output)
    print(f"\n[+] Report written to {path}")


if __name__ == "__main__":
    main()
