#!/usr/bin/env python3
"""Lightweight semantic checks for the v0.6.0 merged skill."""
from pathlib import Path
import sys

REQUIRED_FILES = [
    "SKILL.md",
    "MERGE_DECISION.md",
    "references/knowledge-model.md",
    "references/situated-knowledge.md",
    "references/architecture-atlas.md",
    "references/patterns.md",
    "references/representation.md",
    "references/traceability.md",
    "references/validation.md",
    "references/diagrams/diagram-catalog.md",
    "knowledge-sources/index.yaml",
    "evolution/regression.md",
    "evolution/case-learning.md",
    "cases/gold/README.md",
    "cases/failures/README.md",
]

REQUIRED_MARKERS = [
    "五类知识",
    "Cognitive Spine",
    "六阶段 × 七道闸门",
    "L0–L3",
    "Claim → Evidence → Source Anchor",
    "FACT",
    "INFERENCE",
    "INTERPRETATION",
    "merge",
    "rewrite",
]


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    missing = [p for p in REQUIRED_FILES if not (root / p).is_file()]
    text = (root / "SKILL.md").read_text(encoding="utf-8")
    markers = [m for m in REQUIRED_MARKERS if m not in text]
    if missing or markers:
        print("FAIL: merged capability check failed")
        if missing:
            print("missing files:")
            for p in missing:
                print("  -", p)
        if markers:
            print("missing markers:")
            for m in markers:
                print("  -", m)
        return 1
    print(f"PASS: {len(REQUIRED_FILES)} required asset checks and {len(REQUIRED_MARKERS)} core marker checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
