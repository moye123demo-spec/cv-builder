#!/usr/bin/env python3
"""Validate a CV Builder JSON profile without changing it."""

import argparse
import json
import re
import sys
from pathlib import Path

DATE_RE = re.compile(r"^\d{4}\.\d{2}\s*-\s*(?:\d{4}\.\d{2}|present|至今)$", re.I)
REQUIRED_TOP = ("name", "headline", "target_role", "summary", "contact", "education", "experience", "skills")


def load_profile(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read JSON profile: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError("Profile root must be an object.")
    return value


def validate(profile: dict) -> list[str]:
    errors = []
    for field in REQUIRED_TOP:
        if not profile.get(field):
            errors.append(f"Missing required field: {field}")
    contact = profile.get("contact", {})
    if not isinstance(contact, dict) or not contact.get("email"):
        errors.append("contact.email is required.")
    for section in ("education", "experience"):
        records = profile.get(section, [])
        if not isinstance(records, list) or not records:
            errors.append(f"{section} must be a non-empty list.")
            continue
        for index, record in enumerate(records, start=1):
            if not isinstance(record, dict):
                errors.append(f"{section}[{index}] must be an object.")
                continue
            for field in ("institution", "dates"):
                if not record.get(field):
                    errors.append(f"{section}[{index}].{field} is required.")
            if record.get("dates") and not DATE_RE.match(record["dates"]):
                errors.append(
                    f"{section}[{index}].dates must look like YYYY.MM-YYYY.MM or YYYY.MM-present."
                )
    for index, record in enumerate(profile.get("experience", []), start=1):
        if isinstance(record, dict) and not record.get("title"):
            errors.append(f"experience[{index}].title is required.")
        if isinstance(record, dict) and not record.get("bullets"):
            errors.append(f"experience[{index}].bullets needs at least one verified bullet.")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("profile", type=Path)
    args = parser.parse_args()
    try:
        errors = validate(load_profile(args.profile))
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if errors:
        print("\n".join(f"ERROR: {item}" for item in errors), file=sys.stderr)
        return 1
    print(f"OK: {args.profile} passed profile validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
