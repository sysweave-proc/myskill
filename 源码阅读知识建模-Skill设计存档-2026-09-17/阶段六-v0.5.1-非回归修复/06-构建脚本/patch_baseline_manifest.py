from pathlib import Path
import hashlib, yaml, os
root=Path('C:/Users/zhang/WorkBuddy/2026-09-17-22-06-48/_sandbox6/source-code-reading-skill-v0.5.1')
base=Path('C:/Users/zhang/WorkBuddy/2026-09-17-22-06-48/_sandbox6/_baseline_v0.4')

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
entries=[]
for p in sorted(x for x in base.rglob('*') if x.is_file()):
    rel=str(p.relative_to(base))
    entries.append({'path':rel,'sha256':sha(p)})
(root/'evolution/v0.4-baseline-manifest.yaml').write_text(yaml.safe_dump({'baseline_version':'0.4.0','files':entries},allow_unicode=True,sort_keys=False))
(root/'evolution/approved-changes.yaml').write_text(yaml.safe_dump({'candidate_version':'0.5.1','approved_changed_baseline_files':['SKILL.md','README.md','knowledge-sources/README.md'],'approved_removals':[]},allow_unicode=True,sort_keys=False))

p=root/'tests/test_skill_integrity.py'
t=p.read_text()
t=t.replace('import sys\nfrom pathlib import Path\n', 'import sys\nimport hashlib\nfrom pathlib import Path\nimport yaml\n')
t=t.replace('def main() -> int:\n', '''def sha256(path: Path) -> str:\n    return hashlib.sha256(path.read_bytes()).hexdigest()\n\n\ndef main() -> int:\n''')
# Replace the body from baseline/candidate through return 0
start=t.index('    baseline = Path(sys.argv[1]).resolve()')
end=t.index('\n\nif __name__ ==', start)
body='''    baseline = Path(sys.argv[1]).resolve()\n    candidate = Path(sys.argv[2]).resolve()\n    b = file_set(baseline)\n    c = file_set(candidate)\n\n    policy_path = candidate / "evolution" / "approved-changes.yaml"\n    policy = yaml.safe_load(policy_path.read_text()) if policy_path.exists() else {}\n    approved_changed = set(policy.get("approved_changed_baseline_files", []))\n    approved_removed = set(policy.get("approved_removals", []))\n\n    missing = sorted((b - c) - approved_removed)\n    unexpected_removed = sorted((b - c) - approved_removed)\n    changed = []\n    for rel in sorted(b & c):\n        bp = baseline / rel\n        cp = candidate / rel\n        if sha256(bp) != sha256(cp):\n            changed.append(rel)\n    unexpected_changed = sorted(set(changed) - approved_changed)\n\n    if missing or unexpected_removed or unexpected_changed:\n        print("REGRESSION: baseline preservation failed")\n        if missing:\n            print("Missing baseline files:")\n            for x in missing: print("  -", x)\n        if unexpected_changed:\n            print("Unapproved baseline file content changes:")\n            for x in unexpected_changed: print("  ~", x)\n        return 1\n\n    added = sorted(c - b)\n    print(f"PASS: preserved {len(b)} baseline files; changed {len(changed)} approved baseline files; added {len(added)} files")\n    if changed:\n        print("APPROVED CHANGES:")\n        for x in changed: print("  ~", x)\n    if added:\n        print("ADDED:")\n        for x in added: print("  +", x)\n    return 0\n'''
t=t[:start]+body+t[end:]
p.write_text(t)
