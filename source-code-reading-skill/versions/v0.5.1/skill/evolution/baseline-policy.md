# Skill Evolution Baseline Policy

## Core invariant

**Evolution is merge-based, not rewrite-based.** A new version starts from the previous released asset set and preserves it by default.

## Release procedure

```text
Previous release
      ↓
Capability inventory
      ↓
Baseline file/feature comparison
      ↓
Minimal additive patch
      ↓
Integrity regression
      ↓
Semantic regression
      ↓
Changelog
      ↓
Release
```

## Required checks

### 1. Capability inventory

Record capabilities, reference sets, templates, cases, examples, and tests from the baseline.

### 2. File preservation

Every baseline file must still exist in the candidate unless it appears in an explicit approved-removal record.

### 3. Capability preservation

A file may survive while a capability disappears from it. Therefore compare both file inventory and a human-readable capability inventory.

### 4. Minimal patch

Prefer adding or editing the smallest relevant section. Do not rewrite unrelated references merely to simplify the package.

### 5. Removal protocol

A removal must record:

```yaml
removal:
  path: ""
  capability: ""
  reason: ""
  replacement: ""
  regression_evidence: []
  approved: false
```

### 6. Regression

At minimum run the integrity test plus the semantic regression suite described in `evolution/regression.md`.

## What counts as regression

Examples:

- knowledge-source registry disappears;
- gold/failure cases disappear;
- diagram selection catalog loses critical semantic distinctions;
- trace depth or claim verification disappears;
- document policy becomes too weak to guide a note;
- architecture ↔ topic ↔ source integration is no longer explicit.

## Versioning rule

A corrective release may be `x.y.1` when the main purpose is restoring lost behavior without intentionally redesigning the model.
