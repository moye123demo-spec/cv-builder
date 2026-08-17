#!/usr/bin/env python3
"""Validate anonymous fixtures and generate each supported CV layout."""

import subprocess
import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
PROFILE = REPO / "evals" / "fixtures" / "minimal_candidate.json"
OUT = REPO / "output" / "evals"
JD = REPO / "evals" / "fixtures" / "sample_jd.txt"


def run(*args: str) -> None:
    subprocess.run([sys.executable, *args], check=True)


def main() -> None:
    validate = ROOT / "scripts" / "validate_profile.py"
    generate = ROOT / "scripts" / "generate_resume.py"
    match = ROOT / "scripts" / "match_jd.py"
    run(str(validate), str(PROFILE))
    for template in ("industry-cn", "original-cn", "ats-cn", "academic-cn", "industry-en", "academic-en"):
        run(str(generate), str(PROFILE), "--template", template, "--output", str(OUT / f"{template}.docx"))
    report_path = OUT / "jd-report.json"
    run(str(match), str(PROFILE), str(JD), "--output", str(report_path))
    report = json.loads(report_path.read_text(encoding="utf-8"))
    if report.get("method") != "Rule-based keyword and alias evidence coverage":
        raise RuntimeError("JD report did not identify its rule-based method.")
    print("All template fixtures generated successfully.")


if __name__ == "__main__":
    main()
