#!/usr/bin/env python3
"""Create a transparent, fact-safe JD matching report from a profile and JD text."""

import argparse
import json
import re
from pathlib import Path

from validate_profile import load_profile, validate

KEYWORD_GROUPS = {
    "product": ["product", "产品"],
    "operations": ["operations", "运营"],
    "project management": ["project management", "项目管理", "pmp", "敏捷", "scrum"],
    "sql": ["sql"],
    "tableau": ["tableau"],
    "figma": ["figma"],
    "axure": ["axure"],
    "user research": ["user research", "用户研究", "用户访谈", "可用性测试"],
    "data analysis": ["data analysis", "数据分析", "漏斗分析"],
    "ai": ["ai", "人工智能", "大模型"],
    "growth": ["growth", "增长", "留存"],
    "saas": ["saas"],
    "medical": ["medical", "医疗"],
    "python": ["python"],
    "linux": ["linux"],
    "single-cell": ["single-cell", "单细胞"],
    "bioinformatics": ["bioinformatics", "生物信息"],
}


def normal(text: str) -> str:
    return re.sub(r"\s+", "", text.lower())


def flatten_profile(profile: dict) -> str:
    parts = [profile.get("headline", ""), profile.get("summary", ""), profile.get("target_role", "")]
    for values in profile.get("skills", {}).values():
        parts.extend(values)
    for group in ("experience", "projects", "education"):
        for record in profile.get(group, []):
            if isinstance(record, dict):
                parts.extend(str(v) for v in record.values() if isinstance(v, str))
                parts.extend(record.get("bullets", []))
    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("profile", type=Path)
    parser.add_argument("jd", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    profile = load_profile(args.profile)
    errors = validate(profile)
    if errors:
        raise SystemExit("\n".join(errors))
    jd_text = args.jd.read_text(encoding="utf-8")
    candidate = normal(flatten_profile(profile))
    jd_norm = normal(jd_text)
    jd_terms = [
        canonical for canonical, aliases in KEYWORD_GROUPS.items()
        if any(normal(alias) in jd_norm for alias in aliases)
    ]
    matched = [
        canonical for canonical in jd_terms
        if any(normal(alias) in candidate for alias in KEYWORD_GROUPS[canonical])
    ]
    missing = [term for term in jd_terms if term not in matched]
    coverage = round(100 * len(matched) / len(jd_terms), 1) if jd_terms else 0.0
    report = {
        "target_role": profile["target_role"],
        "method": "Rule-based keyword and alias evidence coverage",
        "interpretation": "This is a tailoring aid, not a prediction of interview or hiring success.",
        "coverage_percent": coverage,
        "jd_keywords_detected": jd_terms,
        "matched_evidence": matched,
        "unverified_or_missing": missing,
        "safe_tailoring_actions": [
            "Move verified matched skills and relevant projects higher in the resume.",
            "Rewrite the headline and summary around the target role using only supplied facts.",
            "Do not add missing keywords unless the candidate confirms the underlying experience."
        ]
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Created JD match report: {args.output} ({coverage}% rule-based coverage; not a hiring score)")


if __name__ == "__main__":
    main()
