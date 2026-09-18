#!/usr/bin/env python3
"""Compare a candidate Skill against a baseline and prevent silent file loss.

Usage:
  python tests/test_skill_integrity.py <baseline_dir> <candidate_dir>

The test intentionally checks preservation rather than requiring byte identity.
"""
from __future__ import annotations
import sys
import hashlib
from pathlib import Path
import yaml


def file_set(root: Path) -> set[str]:
    return {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: test_skill_integrity.py <baseline_dir> <candidate_dir>")
        return 2
    baseline = Path(sys.argv[1]).resolve()
    candidate = Path(sys.argv[2]).resolve()
    b = file_set(baseline)
    c = file_set(candidate)

    policy_path = candidate / "evolution" / "approved-changes.yaml"
    policy = yaml.safe_load(policy_path.read_text()) if policy_path.exists() else {}
    approved_changed = set(policy.get("approved_changed_baseline_files", []))
    approved_removed = set(policy.get("approved_removals", []))

    missing = sorted((b - c) - approved_removed)
    unexpected_removed = sorted((b - c) - approved_removed)
    changed = []
    for rel in sorted(b & c):
        bp = baseline / rel
        cp = candidate / rel
        if sha256(bp) != sha256(cp):
            changed.append(rel)
    unexpected_changed = sorted(set(changed) - approved_changed)

    if missing or unexpected_removed or unexpected_changed:
        print("REGRESSION: baseline preservation failed")
        if missing:
            print("Missing baseline files:")
            for x in missing: print("  -", x)
        if unexpected_changed:
            print("Unapproved baseline file content changes:")
            for x in unexpected_changed: print("  ~", x)
        return 1

    added = sorted(c - b)
    print(f"PASS: preserved {len(b)} baseline files; changed {len(changed)} approved baseline files; added {len(added)} files")
    if changed:
        print("APPROVED CHANGES:")
        for x in changed: print("  ~", x)
    if added:
        print("ADDED:")
        for x in added: print("  +", x)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
