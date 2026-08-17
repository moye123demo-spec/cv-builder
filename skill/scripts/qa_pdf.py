#!/usr/bin/env python3
"""Run lightweight structural checks and optional PNG rendering for a resume PDF."""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from pypdf import PdfReader


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--must-contain", action="append", default=[])
    parser.add_argument("--render-dir", type=Path)
    args = parser.parse_args()
    reader = PdfReader(args.pdf)
    text = "\n".join((page.extract_text() or "") for page in reader.pages)
    missing = [item for item in args.must_contain if item not in text]
    if missing:
        print("ERROR: Missing text: " + ", ".join(missing), file=sys.stderr)
        return 1
    print(f"OK: {len(reader.pages)} page(s), required text found.")
    if args.render_dir:
        converter = shutil.which("pdftoppm")
        if not converter:
            print("WARNING: pdftoppm not found; skipped PNG rendering.", file=sys.stderr)
            return 0
        args.render_dir.mkdir(parents=True, exist_ok=True)
        prefix = args.render_dir / "page"
        subprocess.run([converter, "-png", str(args.pdf), str(prefix)], check=True)
        print(f"Rendered PNGs under: {args.render_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
